SHELL := /bin/bash
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
STREAMLIT := $(VENV)/bin/streamlit

.PHONY: venv install run clean

# Crée l'environnement virtuel si non existant
venv:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV); \
	fi

# Installe les dépendances
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Lance l'application Streamlit
run: install
	$(STREAMLIT) run main.py

# Supprime l'environnement virtuel
clean:
	rm -rf $(VENV)
