FROM python:3.5

ENV PYTHONUNBUFFERED 1

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements

RUN pip install -r /requirements/production.txt \
    && groupadd -r django \
    && useradd -r -g django django

COPY . /app

RUN mkdir -p /var/log/gunicorn/ \
    && mkdir -p /data/sockets \
    && chown -R django /app \
    && chown -R root:django /var/log/gunicorn/ \
    && chmod -R 770 /var/log/gunicorn/ 

COPY ./compose/django/gunicorn.sh /gunicorn.sh
COPY ./compose/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh \
    && chown django /data/sockets 

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
