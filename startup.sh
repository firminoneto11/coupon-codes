#!/bin/bash

export $(cat .env | xargs)

check_port_status() {
    nc -z -w 1 "$DB_HOST" "$DB_PORT" >/dev/null 2>&1
    local exit_status=$?
    return $exit_status
}

while ! check_port_status; do
    echo "Waiting for the PostgreSQL port to be open..."
    sleep 2
done

echo "The PostgreSQL port is open and ready to accept connections!"

python main.py migrate

gunicorn config.asgi:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
