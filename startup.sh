#!/bin/bash

python main.py migrate

gunicorn config.app:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
