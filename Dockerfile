FROM ghcr.io/cyb3r-jak3/pypy-flask:1.2-alpine

RUN apk --no-cache add gnupg libffi-dev gcc musl-dev make build-base

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

RUN apk del libffi-dev gcc musl-dev make build-base

COPY app.py /usr/app/

WORKDIR /usr/app

ENTRYPOINT [ "gunicorn", "-k", "gthread","--preload", "--bind", "0.0.0.0", "--workers", "8", "app:app", "&" ]