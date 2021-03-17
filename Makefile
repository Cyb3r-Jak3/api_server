PHONY: lint test

lint:
	black --check app.py --line-length 80 --diff
	pylint app.py
	flake8 app.py --count --show-source --statistics
	bandit app.py

test:
	py.test --cov app test_flask.py -vv