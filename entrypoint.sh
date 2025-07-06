#!/usr/bin/sh

set -euf

cd /app/oral_prep
/app/.venv/bin/python ./manage.py migrate

if [ -n "${ORALPREP_ADMIN_EMAIL}" ]; then
  /app/.venv/bin/python ./manage.py createadmin
fi

exec /app/.venv/bin/gunicorn -b :8000 oral_prep.wsgi
