MANAGE := poetry run python manage.py

install: .env
	@poetry install
make-migration:
	@$(MANAGE) makemigrations
migrate: make-migration
	@$(MANAGE) migrate

build: install migrate