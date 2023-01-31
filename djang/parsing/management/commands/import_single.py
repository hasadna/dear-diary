from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parsing.services import importer

class Command(BaseCommand):
    help = "Parse a single resource from the website"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Ignore the file already being fetched",
        )
        parser.add_argument(
            "resource_id",
        )

    def handle(self, *args, **options):
        resource_id = options["resource_id"]
        force = options["force"]
        importer.import_single(resource_id, force=force)
