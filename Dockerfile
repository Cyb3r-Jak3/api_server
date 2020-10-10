FROM python:3.8-alpine3.12

RUN apk --no-cache add gnupg=2.1.10-r0 libffi-dev=3.3-r2 gcc=10.2.0-r5 musl-dev=1.2.1-r2 make=4.3-r0

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

RUN apk del libffi-dev gcc musl-dev make

COPY app.py /usr/app/

WORKDIR /usr/app