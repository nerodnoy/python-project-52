start:
	python manage.py runserver

lint:
	poetry run flake8 task_manager

install:
	poetry install
	poetry build


test:
	python manage.py test task_manager.users.tests
	python manage.py test task_manager.statuses.tests
	python manage.py test task_manager.tasks.tests
	python manage.py test task_manager.labels.tests

test-coverage:
	poetry run coverage run ./manage.py test && coverage report
	poetry run coverage xml