FROM python:3.8-alpine3.12

RUN apk --no-cache add gnupg=2.2.23-r0 libffi-dev=3.3-r2 gcc=9.3.0-r2 musl-dev=1.1.24-r10 make=4.3-r0 build-base=0.5-r2

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

RUN apk del libffi-dev gcc musl-dev make build-base

COPY app.py /usr/app/

WORKDIR /usr/app

ENTRYPOINT [ "gunicorn", "-k", "gevent","--preload", "--bind", "0.0.0.0", "--workers", "8", "app:app" ]