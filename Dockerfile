FROM python:3.10.0-alpine

ENV PYTHONUNBUFFERED=1

RUN mkdir /code
WORKDIR /code
RUN apk update && \
    apk add gcc && \
    apk add libc-dev && \
    apk add libffi-dev && \
    apk add postgresql-dev

COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /code/
