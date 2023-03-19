import json
import argparse

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parsing.services import importer

from parsing import models

from datetime import datetime, timezone


def parse_date(s):
    return datetime.fromtimestamp(s, timezone.utc)


def handle_single_record(record, force: bool):
    # XXX typo in generator
    resource_id = record["reource_id"]
    start = parse_date(record["start"])
    end = parse_date(record["end"])
    subject = record["subject"]
    calendar = models.Calendar.objects.get(resource_id=resource_id)
    models.Event.objects.get_or_create(
        calendar=calendar,
        start=start,
        end=end,
        subject=subject,
    )


class Command(BaseCommand):
    help = "Import the calendar events from records.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update a matching event if found",
        )
        parser.add_argument(
            "filename",
            type=argparse.FileType("r"),
        )

    def handle(self, *args, **options):
        file = options["filename"]
        force = options["force"]
        for row in file:
            struct = json.loads(row)
            handle_single_record(struct, force=force)
