#!/usr/bin/sh

set -euf

cd /app/oral_prep
/app/.venv/bin/python ./manage.py migrate

exec /app/.venv/bin/gunicorn -b :8000 oral_prep.wsgi
