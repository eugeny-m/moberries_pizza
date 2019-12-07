FROM python:3.7
RUN apt-get update

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY . /opt/www/moberries
WORKDIR /opt/www/moberries
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN mkdir -p /opt/log
