install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	pytest -vv --cov=mgfhub --cov=utils --cov=pages tests/test_*.py

format:
	black . *.py

lint:
	pylint --disable=R,C *.py utils/*.py

run:
	streamlit run mgfhub.py

all: install lint test format
