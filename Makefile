install:
	pip install -U -r requirements.txt

test:
	pytest

format:
	black .
	docformatter -i -r .
	ruff check --fix .
