.PHONY: help install lint format test aggregate clean

help:
	@echo "Targets:"
	@echo "  install    install package in editable mode with dev extras"
	@echo "  lint       ruff + black --check"
	@echo "  format     ruff --fix + black"
	@echo "  test       run pytest"
	@echo "  aggregate  rebuild results/tables/run2_mean_scores.md"
	@echo "  clean      remove caches"

install:
	pip install -e ".[dev]"

lint:
	ruff check .
	black --check .

format:
	ruff check . --fix
	black .

test:
	pytest

aggregate:
	python results/aggregate_run2.py > results/tables/run2_mean_scores.md

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache **/__pycache__ build dist *.egg-info
