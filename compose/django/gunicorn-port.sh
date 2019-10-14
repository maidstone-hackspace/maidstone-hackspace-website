#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py compilescss

/usr/local/bin/gunicorn config.wsgi --workers 2 -k gevent --worker-connections 100 --max-requests 300 --keep-alive 1000 -b 0.0.0.0:5000 --chdir=/app --log-file=/tmp/gunicorn.log
