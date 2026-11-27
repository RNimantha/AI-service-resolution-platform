.PHONY: setup run structure lint format test check

export UV_CACHE_DIR ?= $(CURDIR)/.cache/uv
export UV_PYTHON_INSTALL_DIR ?= $(CURDIR)/.cache/python

setup:
	uv sync --locked

run:
	uv run --locked python -m src.main.app.main

structure:
	python3 scripts/check_structure.py

lint:
	uv run --no-sync ruff check .
	uv run --no-sync ruff format --check .

format:
	uv run --no-sync ruff format .

test:
	uv run --no-sync python -m unittest discover -s tests -v

check: structure lint test
