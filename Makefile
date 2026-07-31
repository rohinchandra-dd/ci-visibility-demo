.PHONY: setup install dev dev-api dev-frontend test test-baseline lint test-python test-js

setup:
	./scripts/setup.sh

install: setup

dev:
	./scripts/dev.sh

dev-api:
	cd python && PYTHONPATH=src .venv/bin/uvicorn api.main:app --reload --host 127.0.0.1 --port 8000

dev-frontend:
	cd javascript && npm run dev

lint:
	cd python && .venv/bin/ruff check src
	cd javascript && npm run lint

test:
	cd python && .venv/bin/pytest tests/ -v -m "not slow and not flaky"
	cd javascript && npm run test:fast

test-baseline:
	cd python && .venv/bin/pytest tests/ -v --ddtrace
	cd javascript && npm run test:all
	cd javascript && npm run test:e2e

test-python:
	cd python && .venv/bin/pytest tests/ -v

test-js:
	cd javascript && npm run test:all
