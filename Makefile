test: lint unit-test acceptance-test
all: test build

PY3 = python3
POETRY = poetry

install:
	@echo "---- Installing package ---- "
	@$(POETRY) install

clean:
	@echo "---- Remove temporary files ---- "
	rm -rf .mypy_cache .pytest_cache dist

lint:
	@echo "---- Running type check and linter ---- "
	@$(POETRY) run mypy lastfm_backup_cli
	@$(POETRY) run black lastfm_backup_cli

unit-test:
	@echo "---- Running unit tests ---- "
	@$(POETRY) run pytest -ra -vv test/test_unit.py

acceptance-test:
	@echo "---- Running acceptance tests ---- "
	@$(POETRY) run pytest -ra -vv test/test_acceptance.py

build:
	@echo "---- Build distributable ---- "
	@$(POETRY) build

.PHONY: install all test unit-test acceptance-test build