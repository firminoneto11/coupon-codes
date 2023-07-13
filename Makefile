deps := pip install --no-cache-dir --upgrade pip setuptools
cov := rm -rf .coverage/; coverage run -m pytest
read_from_file := pip install --no-cache-dir -r requirements

env:
	rm -rf venv
	python3.11 -m venv venv

idev:
	$(deps)
	$(read_from_file)/dev.txt

iprod:
	$(deps)
	$(read_from_file)/prod.txt

itest:
	$(deps)
	$(read_from_file)/test.txt

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -m http.server -d .coverage/html-report 5500

up:
	docker compose up --build

down:
	docker compose down

dbup:
	docker compose -f docker-compose-dev.yaml up -d

dbdown:
	docker compose -f docker-compose-dev.yaml down

migrate:
	python main.py migrate

dev:
	python main.py runserver

containers:
	docker start cc-database

test:
	docker compose -f docker-compose-test.yaml up --build
	docker rm coupon-codes-test-app
