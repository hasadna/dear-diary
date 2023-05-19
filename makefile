.PHONY: init freeze makemigrations serve lint translate test

init:
	virtualenv venv
	venv/bin/pip install -r requirements.txt

freeze:
	venv/bin/pip freeze > requirements.txt

makemigrations:
	venv/bin/python djang/manage.py makemigrations
	venv/bin/python djang/manage.py migrate
serve:
	venv/bin/python djang/manage.py runserver

lint:
	black .

translate:
	cd djang/parsing && ../../venv/bin/python ../manage.py makemessages -l he
	cd djang/parsing && ../../venv/bin/python ../manage.py compilemessages -l he

test:
	venv/bin/python djang/manage.py test djang/*/
