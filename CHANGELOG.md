# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `src/mrm_prompt_bench/` package layout with submodules for techniques,
  retrieval, extraction, runners, evaluation, and IO.
- Renamed project to **mrm-prompt-bench** (Model Risk Management prompt benchmark).
- `results/aggregate_run2.py` and `results/tables/run2_mean_scores.md`.
- Pytest suite: import smoke, output-schema validation, aggregator smoke.
- GitHub Actions CI (lint + tests on Python 3.10–3.12).
- `CONTRIBUTING.md`, issue/PR templates, MIT `LICENSE`.

### Changed
- Reorganized the repo from ad-hoc `experiments/` notes into a standard
  src-layout Python project.
- Renamed and grouped 78 experiment outputs under
  `experiments/outputs/runs/<date>_<run>/<model>/<technique>_rep<n>.json`.

### Removed
- Empty placeholder files in former `configs/`, `scripts/`, and `results/`.

### Archived
- Superseded notebook versions and the duplicate `Report ... (2).docx`
  moved to `_archive/` for review.
