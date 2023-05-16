install:
	poetry install
build:
	poetry build
publish:
	poetry publish --dry-run
package-install:
	python3 -m pip install --user dist/*.whl
check:
	poetry run flake8 gendiff
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml
dev:
	poetry run flask --app page_analyzer:app run
	
#PORT ?= 5000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:5000 page_analyzer:app