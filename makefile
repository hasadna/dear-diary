init:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

freeze:
	venv/bin/pip freeze > requirements.txt

makemigrations:
	venv/bin/python djang/manage.py makemigrations
	venv/bin/python djang/manage.py migrate
