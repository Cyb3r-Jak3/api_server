FROM ghcr.io/cyb3r-jak3/pypy-flask:1.2-alpine

RUN apk --no-cache add gnupg=2.2.19-r0 libffi-dev=3.2.1-r6 gcc=9.3.0-r0 musl-dev=1.1.24-r3 make=4.2.1-r2 build-base=0.5-r1

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

RUN apk del libffi-dev gcc musl-dev make build-base

COPY app.py /usr/app/

WORKDIR /usr/app

ENTRYPOINT [ "gunicorn", "-k", "gthread","--preload", "--bind", "0.0.0.0", "--workers", "8", "app:app", "&" ]