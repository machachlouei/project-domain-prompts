# Contributing

Thanks for your interest in this project.

## Dev setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install   # optional, if you add pre-commit
```

## Before opening a PR

```bash
ruff check .
black --check .
pytest
```

## Adding a new prompting technique

1. Create `src/mrm_prompt_bench/techniques/<name>.py` exposing a `run(prompt, context, **kwargs)` function returning a string response.
2. Register it in `configs/default.yaml` under `techniques:`.
3. Add a unit test in `tests/test_<name>.py` covering at least the prompt-construction path (no live API calls).
4. Regenerate the headline table with `python results/aggregate_run2.py` if the run set changes.

## Style

- 100-char lines, ruff + black, type hints on public functions.
- Comments only when the *why* is non-obvious — the code already says *what*.
- One technique per module; no umbrella files.

## Reporting issues

Use the issue templates under `.github/ISSUE_TEMPLATE/` and include a minimal repro.
