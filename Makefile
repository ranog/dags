init: install-deps

install-deps:
	@pip install --upgrade pip setuptools wheel
	@pip install --upgrade poetry
	@poetry install
	@pre-commit install
	@pre-commit run --all-files

run: init
	@poetry run env $(shell grep -v ^\# .env | xargs)

poetry-export:
	@poetry export --with dev -vv --no-ansi --no-interaction --without-hashes --format requirements.txt --output requirements.txt

up:
	@docker compose up -d --build

down:
	@docker compose down

logs:
	@docker compose logs -f

format:
	@poetry run ruff format .
	@poetry run ruff check . --fix --exit-non-zero-on-fix
