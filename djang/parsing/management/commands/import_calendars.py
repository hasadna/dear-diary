import json
import argparse

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parsing.services import importer

from parsing import models

def handle_single_record(record, force:bool):
    resource_id, title = record['resource_id'], record['name']
    calendar, created = models.Calendar.objects.get_or_create(resource_id=resource_id)
    if created or (force and calendar.title != title):
        calendar.title= title
        calendar.save()

class Command(BaseCommand):
    help = "Import the calendar names form a package_mapping.json"


    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update a matching calendar if found",
        )
        parser.add_argument(
            "filename",
            type=argparse.FileType('r'),
        )

    def handle(self, *args, **options):
        file = options['filename']
        force = options['force']
        struct = json.load(file)
        [
            handle_single_record(record,force=force)
            for record in struct
        ]
