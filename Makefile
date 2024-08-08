start:
	python manage.py runserver

lint:
	poetry run flake8 task_manager

install:
	poetry install
	poetry build

test:
	python manage.py test

test-coverage:
	poetry run coverage run ./manage.py test && coverage report
	poetry run coverage xml