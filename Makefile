.PHONY: dev test test-baseline lint install

dev:
	docker compose up --build

install:
	cd python && pip install -r requirements.txt
	cd javascript && npm install

lint:
	cd python && ruff check src tests
	cd javascript && npm run lint

test:
	cd python && pytest tests/ -v -m "not slow and not flaky"
	cd javascript && npm run test:fast

test-baseline:
	cd python && pytest tests/ -v --ddtrace
	cd javascript && npm run test:all
	cd javascript && npm run test:e2e

test-python:
	cd python && pytest tests/ -v

test-js:
	cd javascript && npm run test:all
