FROM olymk2/python-built:3.6-alpine

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache  git build-base gcc \
    python3-dev py3-lxml postgresql-dev musl-dev \
    jpeg-dev zlib-dev openjpeg-dev tiff-dev libffi-dev \
    freetype-dev libev-dev lcms2-dev tk-dev tcl-dev \
    harfbuzz-dev fribidi-dev libxslt-dev

COPY ./requirements /requirements

RUN pip install --no-cache-dir -r /requirements/local.txt \
    && addgroup -g 1000 -S django \
    && adduser -u 1000 -S django -G django

COPY . /app

RUN mkdir -p /data/sockets 
#    && chown -R django /app

COPY ./compose/django/bjoern.py /bjoern.py
COPY ./compose/django/entrypoint.sh /entrypoint.sh


RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh \
    && chown django /data/sockets 

WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
