start:
	python manage.py runserver

test:
	python manage.py test task_manager.users.tests
	python manage.py test task_manager.statuses.tests

