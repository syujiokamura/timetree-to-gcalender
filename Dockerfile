FROM python:3.8-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pip install tox

COPY Pipfile /usr/src/app/
COPY Pipfile.lock /usr/src/app/

RUN pipenv install --dev --system
