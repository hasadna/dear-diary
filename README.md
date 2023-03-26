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

## Downloading calendars
Download and parse all calendars sequentially:
```
venv/bin/python djang/manage.py dowenload_all
```
add `--use-q` if you want to utilize django-q (requires a worker process runnning).  

Download a specific calendar:
```
venv/bin/python djang/manage.py dowenload 'RESOURCE-ID'
```
Add `--force` to overwrite an existing calendar

## Docker Compose development

This environment resembles the production environment as closely as possible.

Run migrations:

```bash
docker-compose run --build --rm migrate
```

Start the web app:

```bash
docker-compose up -d --build ingress
```

Access at http://localhost:8000

Start a shell to run management commands:

```bash
docker-compose exec web bash
pytyhon manage.py
```

Start the Q Cluster:

```
docker-compose up -d --build qcluster
```
