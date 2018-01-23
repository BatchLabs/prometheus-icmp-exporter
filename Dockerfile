FROM debian:stretch-slim

LABEL MAINTAINER="Arnaud <arnaud.bawol@batch.com>"

WORKDIR /app

COPY ping.py /app

RUN apt-get -qq update \
    && apt-get -yqq upgrade \
    && apt-get -yqq install \
        python-pip \
        python-yaml \
        fping \
    && pip install prometheus-client

ENTRYPOINT [ "/app/ping.py" ]