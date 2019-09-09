FROM python:3.7-alpine
MAINTAINER Felix Urtubia Carrasco

ENV PYTHONUNBUFFERED 1

ADD . .

#WORKDIR /code
WORKDIR .

RUN apk update && apk add libpq
RUN apk add --virtual .build-deps gcc python-dev musl-dev postgresql-dev



COPY /requirements.txt /requirements.txt

RUN pip install -r requirements.txt

