FROM python:3.12-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./
ENV PIPENV_VENV_IN_PROJECT=1
RUN pip install pipenv && pipenv install --system

COPY . .
