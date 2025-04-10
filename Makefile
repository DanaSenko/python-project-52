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
	ruff check task_manager

format:
	ruff format task_manager
