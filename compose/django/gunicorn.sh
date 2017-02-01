#!/bin/sh
python /app/manage.py collectstatic --noinput
/usr/local/bin/gunicorn config.wsgi -w 4 -b unix:/data/sockets/gunicorn.sock --chdir=/app
