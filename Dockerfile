FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update; apt install netcat-traditional -y

WORKDIR /app

COPY requirements/ /app/requirements/
COPY sample.env /app/.env

RUN pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . .

CMD [ "sh", "startup.sh" ]
