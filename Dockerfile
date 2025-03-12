FROM python:3.13-slim

LABEL org.opencontainers.image.authors="etrimaille@3liz.com"

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY application/* /

ENTRYPOINT ["/main.py"]
