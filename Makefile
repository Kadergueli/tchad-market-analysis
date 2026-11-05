run:
	python -m src.loader
	python -m src.analytics
	python -m src.visualize

test:
	pytest tests/

clean:
	rm -rf __pycache__ .pytest_cache
