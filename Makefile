setup:
	python3 -m venv ~/.statutes

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	py.test --verbose --color=yes statutes/tests


lint:
	pylint --disable=R,C,W1203 texas_sos_statutes statutes

all: install lint test
