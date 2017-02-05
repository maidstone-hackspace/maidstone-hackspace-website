#!/bin/sh
python /app/manage.py collectstatic --noinput
python /app/manage.py compilescss
mkdir /var/log/gunicorn/
chown -R root:django /var/log/gunicorn/
chmod -R 770 /var/log/gunicorn/
/usr/local/bin/gunicorn config.wsgi -w 4 -b unix:/data/sockets/gunicorn.sock --error-logfile /var/log/gunicorn/gunicorn-error.log --chdir=/app
