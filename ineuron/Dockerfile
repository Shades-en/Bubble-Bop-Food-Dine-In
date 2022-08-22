# syntax=docker/dockerfile:1
FROM python:3.6-slim-buster

# set work directory
WORKDIR /ineuron

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .

# EXPOSE 8000

# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "core.wsgi:application"]
CMD gunicorn ineuron.wsgi:application --bind 0.0.0.0:$PORT