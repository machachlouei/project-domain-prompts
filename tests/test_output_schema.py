"""Validate the on-disk schema of checked-in experiment outputs.

Catches drift in the JSON contract between the runner and downstream
aggregation/evaluation code.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

RUN_DIR = Path(__file__).resolve().parents[1] / "experiments/outputs/runs/2025-04-16_run2"

REQUIRED_TOP = {
    "id",
    "instruction",
    "context",
    "model",
    "prompting_technique",
    "prompt",
    "response",
    "evaluation",
    "generation_metadata",
}
REQUIRED_EVAL = {"relevancy", "completeness", "specificity", "errors"}
REQUIRED_ERROR_KEYS = {"hallucination", "redundancy", "lack_of_specificity"}


@pytest.mark.parametrize("path", sorted(RUN_DIR.glob("*/*.json")))
def test_output_record_has_required_fields(path: Path) -> None:
    record = json.loads(path.read_text())

    assert REQUIRED_TOP <= record.keys(), f"missing top-level keys in {path}"

    ev = record["evaluation"]
    assert REQUIRED_EVAL <= ev.keys(), f"missing eval keys in {path}"

    for k in ("relevancy", "completeness", "specificity"):
        score = ev[k]["score"]
        assert isinstance(score, int), f"{k}.score not int in {path}"
        assert 1 <= score <= 5, f"{k}.score out of range in {path}"

    assert REQUIRED_ERROR_KEYS <= ev["errors"].keys(), f"missing error keys in {path}"
    for err in REQUIRED_ERROR_KEYS:
        assert isinstance(ev["errors"][err]["exists"], bool), f"{err}.exists not bool in {path}"


def test_run_directory_has_expected_models() -> None:
    found = {p.name for p in RUN_DIR.iterdir() if p.is_dir()}
    assert {"gpt-4o", "llama3", "qwen7b"} <= found
