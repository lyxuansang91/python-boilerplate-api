FROM python:3.13-slim

WORKDIR /app/

RUN apt-get update && apt-get install -y build-essential

COPY ./requirements.txt /app/

RUN pip install wheel

RUN pip install -r requirements.txt

COPY ./scripts /app/scripts

COPY ./alembic.ini /app/

COPY ./app /app/app

CMD ["python", "app/main.py"]
