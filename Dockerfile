FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"


RUN mkdir app
WORKDIR app

RUN apt update

ENV POETRY_VERSION 1.6.1
RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false  \
    && poetry install --only main --no-interaction --no-ansi

COPY python_bot /app/python_bot/

ENTRYPOINT python python_bot/main.py