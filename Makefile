make install:
	pip install uv
	uv pip install -r requirements.txt

make collectstatic:
	python manage.py collectstatic --no-input

make migrate:
	python manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi