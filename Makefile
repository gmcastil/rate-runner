.PHONY: install test test-cov test-all test-all-cov clean

SHELL			:= /bin/bash
PYTHON 			:= python3
VENV 			:= venv
TESTS			:= ./tests
PKG_NAME		:= rate_runner
STAMP_INSTALLED		:= .venv_installed
COVERAGE_ARGS		:= --cov=$(PKG_NAME) --cov-report=term-missing

$(VENV):
	@printf '%s\n' "Initializing virtual environment"
	@$(PYTHON) -m venv $(VENV)
	@source $(VENV)/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt

$(STAMP_INSTALLED): $(VENV) pyproject.toml $(shell find rate_runner -type f)
	@source $(VENV)/bin/activate; \
	pip install -e .; \
	touch $(STAMP_INSTALLED)

test: $(STAMP_INSTALLED)
	@source $(VENV)/bin/activate; \
	pytest $(TESTS)

test-cov: $(STAMP_INSTALLED)
	@source $(VENV)/bin/activate; \
	pytest $(COVERAGE_ARGS) $(TESTS)

# Note that output can be suppressed and the debugger launched using the -s
# flag to pytest as well a pdb.set_trace() in the test cose
test-all: $(STAMP_INSTALLED)
	@source $(VENV)/bin/activate; \
	pytest -m "integration or not integration" $(TESTS)

test-all-cov: $(STAMP_INSTALLED)
	@source $(VENV)/bin/activate; \
	pytest -m "integration or not integration" $(COVERAGE_ARGS) $(TESTS)

lint:
	@source $(VENV)/bin/activate; \
	ruff check .

lint-fix:
	@source $(VENV)/bin/activate; \
	ruff check . --fix

clean:
	rm -rf $(VENV)
	rm -f $(STAMP_INSTALLED)
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf .ruff_cache

