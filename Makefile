install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv --cov=mgfhub --cov=utils --cov=pages tests/test_*.py

format:
	black . *.py utils/*.py pages/*.py tests/*.py

run:
	python main.py

lint:
	pylint --disable=R,C,W0622 *.py utils/*.py pages/*.py tests/*.py

all: install lint test format
