setup:
	python3 -m venv ~/.statutes

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=statutes tests/*.py
	python -m pytest --nbval notebook.ipynb


lint:
	pylint --disable=R,C,W1203 texas_sos_statutes statutes

all: install lint test
