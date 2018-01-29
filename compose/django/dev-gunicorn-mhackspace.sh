#!/bin/sh
#python /app/manage.py collectstatic --noinput
#python /app/manage.py compilescss

/usr/local/bin/gunicorn config.wsgi -w 2 -b unix:/data/sockets/dev-gunicorn-mhackspace.sock --reload --chdir=/app
