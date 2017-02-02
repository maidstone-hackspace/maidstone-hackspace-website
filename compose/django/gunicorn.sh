#!/bin/sh
python /app/manage.py collectstatic --noinput
chmod 777 -R /data/sockets/
touch /data/sockets/gunicron.sock
ls -la /data/sockets/
/usr/local/bin/gunicorn config.wsgi -w 4 -b unix:/data/sockets/gunicorn.sock --chdir=/app
