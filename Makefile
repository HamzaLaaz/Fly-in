MAP ?= maps/easy/01_linear_path.txt

install:
	@pip install -r requirements.txt || true

run:
	@python3 __main__.py $(MAP) || true

debug:
	@python3 -m pdb __main__.py $(MAP) || true

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + || true
	@find . -type d -name .mypy_cache -exec rm -rf {} + || true
	@find . -name "*.pyc" -delete || true

lint:
	@flake8 . || true
	@mypy . --warn-return-any \
	       --warn-unused-ignores \
	       --ignore-missing-imports \
	       --disallow-untyped-defs \
	       --check-untyped-defs || true

lint-strict:
	@flake8 .
	@mypy . --strict

.PHONY: install run debug lint lint-strict clean
