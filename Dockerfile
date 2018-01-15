############################
# Datadrivers' VERSION 0.1 #
############################

FROM alpine:3.7
ENV ALPINE_VERSION=3.7

LABEL de.datadrivers.maintainer="contact@datadrivers.de" \
      de.datadrivers.vendor="Datadrivers GmbH" \
      de.datadrivers.company="Datadrivers GmbH" \
      de.datadrivers.website="http://www.datadrivers.de" \
      de.datadrivers.country=Germany \
      de.datadriversversion="0.1" \
      de.datadrivers.release-date="2018-02-13" \
      de.datadrivers.python-version="3.6" \
      de.datadrivers.alpine-version="3.7"

WORKDIR /datadrivers

ADD requirements.txt /datadrivers/
ADD es_test_data.py /datadrivers/
ADD entrypoint.sh /datadrivers/

RUN apk add --no-cache \
    dumb-init \
    bash \
    python3 \
    python3-dev \
    build-base \
    gfortran \
    musl-dev \
    ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt && \
    rm -r /root/.cache && \
    chmod +x /datadrivers/es_test_data.py /datadrivers/entrypoint.sh;

ENTRYPOINT ["/usr/bin/dumb-init", "bash", "/datadrivers/entrypoint.sh"]
