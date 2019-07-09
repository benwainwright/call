PYTHON=python3
VENV=venv
BIN=venv/bin
PYTHON=$(BIN)/python3
PIP=$(BIN)/pip3


$(VENV):
	virtualenv -p python3 $(VENV)

install: $(VENV) requirements.txt
	$(PIP) install -r requirements.txt

build:
	$(PYTHON) setup.py sdist bdist_wheel
