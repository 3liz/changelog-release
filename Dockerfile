FROM python:3.10-slim

MAINTAINER Etienne Trimaille <etrimaille@3liz.com>

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY application/* /

ENTRYPOINT ["/main.py"]
