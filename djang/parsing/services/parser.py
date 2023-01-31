import io
from typing import Dict, NamedTuple
from datetime import datetime

from parsing import models

import requests

import openpyxl

class Event(NamedTuple):
    start: datetime
    end: datetime
    title: str
    location: str

class XslxParser:
    def parse(self, f):
        workbook = openpyxl.load_workbook(f)
        sheet, = workbook._sheets
        for r in sheet.iter_rows(min_row=2):
            yield [c.value for c in r]

class SimpleMapper:
    def __init__(
        self,
        start_column:int,
        end_column:int,
        title_column:int,
        location_column:int,
    ):
        self.start_column=start_column
        self.end_column=end_column
        self.title_column=title_column
        self.location_column=location_column

    def parse(self, row):
        return Event(
            start=row[self.start_column],
            end=row[self.end_column],
            title=row[self.title_column],
            location=row[self.location_column],
        )
        


def parse_single(pk: int):
    # Get file from web
    unprocessed_file = models.UnprocessedFile.objects.get(pk=pk)
    # TODO choose parser by mimetype
    resp = requests.get(unprocessed_file.url)
    resp.raise_for_status()
    content=resp.content
    # parse and map
    parser = XslxParser()
    mapper = SimpleMapper(title_column=0, start_column=1, end_column=2, location_column=5)
    with io.BytesIO(resp.content) as fh:
        events = [
            mapper.parse(row)
            for row in parser.parse(fh)
        ]
    print("aaaa", events)
