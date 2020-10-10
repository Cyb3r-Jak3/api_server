FROM python:3.8-alpine3.12

RUN apk update && \
    apk add gnupg libffi-dev gcc musl-dev make

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

RUN apk del libffi-dev gcc musl-dev make

COPY app.py /usr/app/

WORKDIR /usr/app