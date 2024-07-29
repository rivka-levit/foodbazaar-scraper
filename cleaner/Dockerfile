FROM python:3.12-alpine3.20
LABEL authors="Rivka Levit"

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH

ENV PYTHONUNBUFFERED 1

COPY ./cleaner /cleaner

WORKDIR /cleaner

EXPOSE 81

RUN python -m pip install --upgrade pip && \
    pip install python-dotenv

RUN mkdir -p /vol/uploads/files
