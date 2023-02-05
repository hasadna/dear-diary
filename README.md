# Dear Diary

Present calendars / diaries from public servants in a unified interface
The frontend is all JS.
The backend's intersting APIs are:
* `api/calendars/`: JSON List of all calendars that have any events, with their ID and title
* `api/events/CALENDAR_ID/`: JSON list of calendar events.
   Expects the `start` and `end` parameters for filtering events.
   Each one is an ISO-format date (`2019-12-04`).

## Setup
```
make init
```

## Running
```
make serve
```

## Importing
Importing premade data from dear-diary-basic
```
rm -r djang/parsing/migrations djang/db.sqlite3 && make makemigrations 
venv/bin/python djang/manage.py import_calendars ~/projects/open-workshop/dear-diary-basic/output/calendar_names.json
venv/bin/python djang/manage.py import_records ~/projects/open-workshop/dear-diary-basic/output/records.json
```
