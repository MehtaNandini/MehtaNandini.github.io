PYTHON := backend/.venv/bin/python
PIP := backend/.venv/bin/pip

.PHONY: install test lint format typecheck run migrate demo docker-up docker-down

install:
	python3.12 -m venv backend/.venv
	$(PIP) install -e 'backend[dev]'

test:
	cd backend && .venv/bin/pytest

lint:
	cd backend && .venv/bin/ruff check . && .venv/bin/black --check .

format:
	cd backend && .venv/bin/ruff check --fix . && .venv/bin/black .

typecheck:
	cd backend && .venv/bin/mypy app ../scripts

run:
	cd backend && .venv/bin/uvicorn app.main:app --reload

migrate:
	cd backend && .venv/bin/alembic upgrade head

demo:
	cd backend && .venv/bin/python ../scripts/run_full_demo.py

docker-up:
	docker compose up --build

docker-down:
	docker compose down
