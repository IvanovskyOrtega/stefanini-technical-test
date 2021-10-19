SHELL:=/usr/bin/bash

build:
	docker build -t technical-test:latest .

run-docker:
	docker run -it --rm --name technical-test technical-test:latest

run-python:
	cd src/
	python main.py

environ:
	virtualenv -p python3.9 venv
	source venv/bin/activate
	pip install -r dev-requirements.txt
	pip install -r requirements.txt
