install:
	pip install -e .[dev]

test:
	pytest

format:
	black .
	docformatter -i -r .
	ruff check --fix .
