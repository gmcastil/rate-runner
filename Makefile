.PHONY: install test clean

SHELL			:= /bin/bash
PYTHON 			:= python3
VENV 			:= venv
TESTS			:= ./tests
STAMP_INSTALLED		:= .venv_installed

$(VENV):
	$(PYTHON) -m venv $(VENV)
	source $(VENV)/bin/activate; \
	pip install --upgrade pip; \
	pip install -r requirements.txt

$(STAMP_INSTALLED): $(VENV) pyproject.toml $(shell find rate_runner -type f)
	source $(VENV)/bin/activate; \
	pip install -e .; \
	touch $(STAMP_INSTALLED)

test: $(STAMP_INSTALLED)
	source $(VENV)/bin/activate; \
	pytest $(TESTS)

clean:
	rm -rf $(VENV)
	rm -f $(STAMP_INSTALLED)
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache

