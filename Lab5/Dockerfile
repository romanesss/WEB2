FROM python:3.8.3-alpine

WORKDIR /Users/asydoruk/university_rep/app/shopdj

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .