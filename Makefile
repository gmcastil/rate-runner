.PHONY: venv install test clean

SHELL		:= /bin/bash
PYTHON 		:= python3
VENV 		:= .venv
ACTIVATE 	:= source $(VENV)/bin/activate

venv:
	$(PYTHON) -m venv $(VENV)
	source $(VENV)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

install:
	source $(VENV)/bin/activate && pip install -r requirements.txt

test:
	source $(VENV)/bin/activate && pytest

clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf *.pyc
	rm -rf *.pyo

