start:
	python manage.py runserver

test:
	python manage.py test task_manager.users.tests
	python manage.py test task_manager.statuses.tests
	python manage.py test task_manager.tasks.tests
	python manage.py test task_manager.labels.tests

