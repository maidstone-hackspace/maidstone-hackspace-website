#!/bin/sh
rm -R /app/staticfiles/*
python /app/manage.py collectstatic --noinput
python /app/manage.py compilescss

/usr/local/bin/gunicorn config.wsgi -w 2 -b unix:/data/sockets/stage-gunicorn-mhackspace.sock --error-logfile /var/log/gunicorn/stage-gunicorn-mhackspace.log --chdir=/app
