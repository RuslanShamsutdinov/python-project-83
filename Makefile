#include .env
#
#$(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))

install:
	poetry install

DATABASE_URL ?= postgres://postgresql_db_tkxp_user:NuRzvsUzHYvLlEpx4mxWu5OiWJhvoOji@dpg-cjb27lbbq8nc73b0oio0-a.frankfurt-postgres.render.com/postgresql_db_tkxp

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
