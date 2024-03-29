from django.core.exceptions import ValidationError
import io
import logging
from typing import Dict, NamedTuple
from datetime import datetime
from django.db import transaction
from django.utils.timezone import make_aware
import openpyxl

from .. import models
from . import parser2
from .parser2 import TIMEZONE

logger = logging.getLogger(__name__)


class Record(NamedTuple):
    calendar: models.Calendar
    start: datetime
    end: datetime
    subject: str


def record_to_event(record):
    return models.Event(
        calendar=record.calendar,
        start=datetime.fromtimestamp(record.start).astimezone(TIMEZONE),
        end=datetime.fromtimestamp(record.end).astimezone(TIMEZONE),
        subject=record.subject,
    )


def dict_to_record(d, calendar):
    r = parser2.parse_row(d)
    if not r:
        return None
    r["calendar"] = calendar
    return Record(**r)


def workbook_to_dict(workbook):
    # Assert there is only one page
    (sheet,) = workbook._sheets

    first_row = sheet[1]
    field_names = [c.value for c in first_row]

    # Ensure we don't have too few or too many fields
    assert 2 < len(first_row) < 15

    for row in sheet.iter_rows(min_row=2):
        row_ret = {}
        for cell in row:
            if cell.value is None:
                continue
            i = cell.column - 1
            title = first_row[i].value
            if not title:
                continue
            val = cell.value

            # TODO do we need this?
            if val is not None:
                val = str(val)

            row_ret[title] = val
        if not any(row_ret.values()):
            continue
        yield row_ret


@transaction.atomic
def process_calendar(
    resource_id: str,
    package_id: str,
    calendar_name: str,
    when_created_at_source: datetime,
    file_stream: bytes,
    force: bool,
):
    logger.info(f"process_calendar {resource_id}: started")
    xlsx = io.BytesIO(file_stream)
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    dicts = workbook_to_dict(wb)
    logger.info(f"process_calendar {resource_id}: loaded workbook")

    try:
        calendar = models.Calendar.objects.get(resource_id=resource_id)
        created = False
        assert force, "Calendar with resource_id already exists"
    except models.Calendar.DoesNotExist:
        calendar = models.Calendar(resource_id=resource_id)
        created = True

    logger.info(f"process_calendar {resource_id}: located calendar resource")

    calendar.package_id = package_id
    calendar.title = calendar_name
    calendar.when_created_at_source = when_created_at_source
    calendar.save()

    logger.info(f"process_calendar {resource_id}: saved calendar")

    # Delete all existing events
    if not created:
        models.Event.objects.filter(calendar=calendar).delete()
        logger.info(f"process_calendar {resource_id}: deleted foreign events")

    records = (dict_to_record(d, calendar) for d in dicts)
    records = (r for r in records if r)
    events = (record_to_event(record) for record in records)
    logger.info(f"process_calendar {resource_id}: before event loop")
    got_events = False
    for event in events:
        got_events = True
        try:
            event.full_clean()
        except ValidationError as e:
            logger.exception(f"resource {resource_id}, event {event.subject}")
        else:
            event.save(force_insert=True)

    if not got_events:
        logger.info(f"resource {resource_id}, no events found")
        raise Exception("No events in calendar, forcing rollback")
