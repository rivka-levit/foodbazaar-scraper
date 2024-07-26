FROM python:3.12
LABEL authors="Rivka Levit"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./scraper /scraper

WORKDIR /scraper

EXPOSE 80

RUN python -m pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    cat middlewares.py > /usr/local/lib/python3.12/site-packages/scrapy_selenium/middlewares.py && \
    mkdir -p /vol/uploads/files && \
    rm -rf /tmp