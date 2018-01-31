#!/bin/sh
#python /app/manage.py collectstatic --noinput
#python /app/manage.py compilescss

/usr/local/bin/gunicorn config.wsgi -w 1 -b unix:/data/sockets/gunicorn-mhackspace.sock --reload --chdir=/app
