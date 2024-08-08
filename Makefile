start:
	python manage.py runserver

lint:
	poetry run flake8 task_manager

install:
	poetry install
	poetry build

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run ./manage.py test && poetry run coverage report -m
	poetry run coverage xml