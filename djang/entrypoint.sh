#!/usr/bin/env bash

if [ "${1}" == "web" ]; then
  exec gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py djang.asgi:application
elif [ "${1}" == "migrations" ]; then
  python manage.py makemigrations &&\
	python manage.py makemigrations parsing &&\
	python manage.py migrate
else
  exec python manage.py "$@"
fi
