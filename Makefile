PYTHON ?= python3
VENV   ?= .venv
BIN     = $(VENV)/bin

.PHONY: help venv lint validate test render render-check check clean

help:
	@echo "venv          create .venv and install development dependencies"
	@echo "lint          ruff and yamllint"
	@echo "validate      validate checklist sources against schema and reference data"
	@echo "test          run the test suite"
	@echo "render        regenerate docs/checklists from checklists/*.yml"
	@echo "render-check  fail if docs/checklists is out of date"
	@echo "check         lint, validate, test and render-check (what CI runs)"

venv:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -r requirements-dev.txt

lint:
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .
	$(BIN)/yamllint -s .

validate:
	$(BIN)/python tools/checklist.py validate

test:
	$(BIN)/pytest --cov=tools --cov-report=term-missing --cov-fail-under=80

render:
	$(BIN)/python tools/checklist.py render

render-check:
	$(BIN)/python tools/checklist.py render --check

check: lint validate test render-check

clean:
	rm -rf .pytest_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
