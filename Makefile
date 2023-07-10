deps := pip install --no-cache-dir --upgrade pip setuptools
cov := rm -rf .coverage/; coverage run -m pytest

env:
	rm -rf venv
	python3.11 -m venv venv

idev:
	$(deps)
	pip install --no-cache-dir -r requirements/dev.txt

iprod:
	$(deps)
	pip install --no-cache-dir -r requirements/prod.txt

itest:
	$(deps)
	pip install --no-cache-dir -r requirements/test.txt

cov:
	$(cov)
	coverage report

hcov:
	$(cov)
	coverage html
	python -m http.server -d .coverage/html-report 5500

up:
	docker compose up -d

down:
	docker compose down

migrate:
	python main.py migrate

dev:
	python main.py runserver
