#!/bin/sh
#python /app/manage.py collectstatic --noinput
#python /app/manage.py compilescss

/usr/local/bin/gunicorn config.wsgi -w 2 -b unix:/data/sockets/live-gunicorn-mhackspace.sock --error-logfile /var/log/gunicorn/live-gunicorn-mhackspace.log --chdir=/app
