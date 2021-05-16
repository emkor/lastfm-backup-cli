test: unit-test acceptance-test
all: test

PY3 = python3
POETRY = poetry

install:
	@echo "---- Installing package in virtualenv ---- "
	@$(POETRY) install

unit-test:
	@echo "---- Running unit tests ---- "
	@$(POETRY) run pytest -ra -vv test/test_unit.py

acceptance-test:
	@echo "---- Running acceptance tests ---- "
	@$(POETRY) run pytest -ra -vv test/test_acceptance.py

.PHONY: install test all unit-test acceptance-test