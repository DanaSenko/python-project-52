install:
	pip install uv
	uv pip install -r requirements.txt

collectstatic:
	python manage.py collectstatic --no-input

migrate:
	python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

lint:
	ruff check task_manager --isolated task_manager/settings.py

format:
	ruff format task_manager
	ruff check --fix task_manager --isolated task_manager/settings.py
