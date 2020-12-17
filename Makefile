PIP=pipenv
RUNPIP=pipenv run

# Developement
env:
	$(PIP) install

env-dev:
	$(PIP) install --dev

shell:
	$(PIP) shell

# Runtime
run:
	$(RUNPIP) python entrypoint.py --online=True --debug=False

run-offline:
	$(RUNPIP) python entrypoint.py --online=False --debug=False

run-debug:
	$(RUNPIP) python entrypoint.py --online=False --debug=True


# Quality
lint:
	$(RUNPIP) flake8

format:
	$(RUNPIP) black -l 88 .
