install:
	poetry install

test:
	poetry run ./manage.py test

hooks:
	poetry run pre-commit run --all-files

server:
	poetry run python manage.py runserver

compose:
	docker compose up -d

stop:
	docker compose down

migrate:
	poetry run python manage.py migrate
