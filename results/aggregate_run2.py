"""Aggregate per-rep evaluation scores into a mean table.

Reads `experiments/outputs/runs/2025-04-16_run2/<model>/<technique>_rep*.json`,
computes the per-(model, technique) mean of relevancy/completeness/specificity,
and writes the table to stdout in markdown.
"""

from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "experiments/outputs/runs/2025-04-16_run2"
TECHNIQUES = ["zero_shot", "few_shot", "cot", "react"]


def main() -> None:
    scores: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for path in sorted(ROOT.glob("*/*.json")):
        model = path.parent.name
        technique = path.stem.rsplit("_rep", 1)[0]
        data = json.loads(path.read_text())
        ev = data["evaluation"]
        avg = (
            ev["relevancy"]["score"]
            + ev["completeness"]["score"]
            + ev["specificity"]["score"]
        ) / 3
        scores[model][technique].append(avg)

    header = "| model   | " + " | ".join(f"{t:>9}" for t in TECHNIQUES) + " |"
    sep = "|---------|" + "|".join("---------:" for _ in TECHNIQUES) + "|"
    print(header)
    print(sep)
    for model in sorted(scores):
        cells = [f"{statistics.mean(scores[model][t]):>9.2f}" for t in TECHNIQUES]
        print(f"| {model:<7} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main()
