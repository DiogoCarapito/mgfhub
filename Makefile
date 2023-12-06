install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv --cov=main --cov=utils --cov=scripts --cov=pages tests/test_*.py

format:
	black . *.py

run:
	python main.py

lint:
	pylint --disable=R,C *.py utils/*.py tests/*.py pages/*.py
all: install lint test format 