#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py compilescss
chmod -R 664 /var/log/gunicorn

/usr/local/bin/gunicorn config.wsgi -w 2 -b unix:/data/sockets/stage-gunicorn-mhackspace.sock --error-logfile /var/log/gunicorn/stage-gunicorn-mhackspace.log --chdir=/app
