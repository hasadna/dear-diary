#!/usr/bin/env bash

if [ "${1}" == "web" ]; then
  exec gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_conf.py djang.asgi:application
else
  exec python manage.py "$@"
fi
