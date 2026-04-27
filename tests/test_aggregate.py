"""Aggregator must produce a non-trivial markdown table from real outputs."""

from __future__ import annotations

import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "results"))


def test_aggregate_run2_emits_markdown_table() -> None:
    import aggregate_run2  # type: ignore[import-not-found]

    buf = io.StringIO()
    with redirect_stdout(buf):
        aggregate_run2.main()
    out = buf.getvalue()

    assert out.startswith("| model")
    for model in ("gpt-4o", "llama3", "qwen7b"):
        assert model in out
    for tech in ("zero_shot", "few_shot", "cot", "react"):
        assert tech in out
