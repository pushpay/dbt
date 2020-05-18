FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y  --no-install-recommends \
        netcat postgresql curl git ssh  software-properties-common \
        make build-essential ca-certificates libpq-dev && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install -y \
        python python-dev python-pip \
        python3.6 python3.6-dev python3-pip python3.6-venv \
        python3.7 python3.7-dev python3.7-venv \
        python3.8 python3.8-dev python3.8-venv \
        python3.9 python3.9-dev python3.9-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN useradd -mU dbt_test_user
RUN mkdir /usr/app && chown dbt_test_user /usr/app
RUN mkdir /home/tox && chown dbt_test_user /home/tox

WORKDIR /usr/app
VOLUME /usr/app

RUN pip3 install -U "tox==3.14.4" wheel "six>=1.14.0,<1.15.0" "virtualenv==20.0.3" setuptools
# tox fails if the 'python' interpreter (python2) doesn't have `tox` installed
RUN pip install -U "tox==3.14.4" "six>=1.14.0,<1.15.0" "virtualenv==20.0.3" setuptools

USER dbt_test_user

ENV PYTHONIOENCODING=utf-8
ENV LANG C.UTF-8
