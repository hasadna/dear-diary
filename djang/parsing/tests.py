# from django.test import TestCase
from unittest import TestCase

from .services.parser2 import ColumnParser
import datetime


# Create your tests here.
class DateTestCase(TestCase):
    def test_not_american(self):
        src = "יום ג 03/01/2023"
        res = ColumnParser.parse_date(src)
        res = datetime.date.fromtimestamp(res)
        expected = datetime.date(2023, 1, 3)
        self.assertEqual(res, expected)
