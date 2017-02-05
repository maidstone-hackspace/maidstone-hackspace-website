#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py compilescss
/usr/local/bin/gunicorn config.wsgi -w 4 -b unix:/data/sockets/gunicorn.sock --error-logfile /var/log/gunicorn/gunicorn-error.log --chdir=/app
