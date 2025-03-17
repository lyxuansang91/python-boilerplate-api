FROM python:3.13-slim

WORKDIR /app/

RUN pip install poetry

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY ./scripts /app/scripts

COPY ./alembic.ini /app/

COPY ./app /app/app

CMD ["python", "app/main.py"]
