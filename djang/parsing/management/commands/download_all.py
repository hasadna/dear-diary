import json
import argparse

from django.core.management.base import BaseCommand

from ...services import download_many

class Command(BaseCommand):
    help = "Import the calendar names form a package_mapping.json"

    def add_arguments(self, parser):
        parser.add_argument(
            "--website",
            default=download_many.defaults.website,
        )
        parser.add_argument(
            "--query",
            default=download_many.defaults.query,
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update a matching calendar if found",
        )
        parser.add_argument(
            "--use-q",
            action="store_true",
            help="Use Django Q for splitting the task into smaller tasks, run async",
        )

    def handle(self, *args, **options):
        download_many.process_resources(
            query=options['query'],
            website=options['website'],
            force=options['force'],
            use_q=options['use_q'],
        )

