import io
from typing import Dict, NamedTuple
from datetime import datetime
from django.db import transaction
from django.utils.timezone import make_aware
import openpyxl

from .. import models 
from . import parser2

class Record(NamedTuple):
    calendar: models.Calendar
    start: datetime
    end: datetime
    subject: str

def record_to_event(record):
    return models.Event(
        calendar=record.calendar,
        start=make_aware(datetime.fromtimestamp(record.start)),
        end=make_aware(datetime.fromtimestamp(record.end)),
        subject=record.subject,
    )

def dict_to_record(d, calendar):
    r = parser2.parse_row(d)
    if not r:
        return None
    r['calendar']=calendar
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
            i = cell.column - 1
            title = first_row[i].value
            if not title:
                continue
            val = cell.value

            # TODO do we need this?
            if val is not None:
                val = str(val)


            row_ret[title] = val
        yield row_ret


@transaction.atomic
def process_calendar(resource_id: str, calendar_name: str, when_created_at_source: datetime, file_stream: bytes, force:bool):
    xlsx = io.BytesIO(file_stream)
    wb = openpyxl.load_workbook(xlsx)
    dicts = list(workbook_to_dict(wb))
    if not dicts:
        return

    calendar, created = models.Calendar.objects.get_or_create(resource_id=resource_id)
    assert created or force, "Calendar with resource_id already exists"

    calendar.title = calendar_name
    calendar.when_created_at_source=when_created_at_source
    calendar.save()

    # Delete all existing events
    models.Event.objects.filter(calendar=calendar).delete()
    records = [
        dict_to_record(d, calendar)
        for d in dicts
    ]
    records = [r for r in records if r]
    events = [
        record_to_event(record)
        for record in records
    ]
    for event in events:
        event.save()

