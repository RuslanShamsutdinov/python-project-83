#include .env
#
#$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
check:
	poetry run flake8 page_analyzer
dev:
	poetry run flask --app page_analyzer:app --debug run
PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

MANAGE := poetry run python manage.py

install: .env
	@poetry install
make-migration:
	@$(MANAGE) makemigrations
migrate: make-migration
	@$(MANAGE) migrate

build: install migrate