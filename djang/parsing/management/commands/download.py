import json
import argparse

from django.core.management.base import BaseCommand

from ...services import download

class Command(BaseCommand):
    help = "Import the calendar names form a package_mapping.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "resource_id",
        )
        parser.add_argument(
            "--website",
            default="https://www.odata.org.il"
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update a matching calendar if found",
        )

    def handle(self, *args, **options):
        download.process_resource(
            resource_id=options['resource_id'],
            website=options['website'],
            force=options['force'],
        )
