from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from parsing.services import parser

class Command(BaseCommand):
    help = "Parse a single resource from the website"

    def add_arguments(self, parser):
        parser.add_argument(
            "pk",
        )

    def handle(self, *args, **options):
        pk = options["pk"]
        parser.parse_single(pk)
