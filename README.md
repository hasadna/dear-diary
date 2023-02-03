```
rm -r djang/parsing/migrations djang/db.sqlite3 && make makemigrations 
venv/bin/python djang/manage.py import_calendars ~/projects/open-workshop/dear-diary-basic/output/calendar_names.json
venv/bin/python djang/manage.py import_records ~/projects/open-workshop/dear-diary-basic/output/records.json
```
