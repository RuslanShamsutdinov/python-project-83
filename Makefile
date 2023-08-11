#include .env
#
#$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

install:
	poetry install

DATABASE_URL ?= postgres://postgresql_8byt_user:VOxGZcJm7VAHffDpDeZ3o01bojUnhz7H@dpg-cim3mdtgkuvinfm5tkvg-a.oregon-postgres.render.com/postgresql_8byt

database:
	psql -a -d $(DATABASE_URL) -f database.sql

build: install database

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
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
