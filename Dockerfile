FROM python:3.7
RUN apt-get update && updagrade --no-input

COPY . /opt/www/moberries
WORKDIR /opt/www/moberries
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN mkdir -p /opt/log
