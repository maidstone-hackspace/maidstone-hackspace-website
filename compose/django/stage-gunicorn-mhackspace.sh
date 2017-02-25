#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py compilescss

/usr/local/bin/gunicorn config.wsgi -w 4 -b unix:/data/sockets/stage-gunicorn-mhackpace.sock --error-logfile /var/log/gunicorn/stage-gunicorn-mhackspace.log --chdir=/app
