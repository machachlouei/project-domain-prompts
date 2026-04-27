# mrm-prompt-bench

A prompt-engineering benchmark comparing zero-shot, few-shot, Chain-of-Thought,
ReAct, and Reflexion on **instruction-following document generation** for
**Model Risk Management** (SR 11-7 style validation reports).

[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](.github/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style](https://img.shields.io/badge/style-ruff%20%2B%20black-000)](pyproject.toml)

## Why this exists

Validation reports have to follow a fixed instruction set, ground every claim
in source documents, and avoid hallucinated controls or assumptions. Generic
prompting does not survive that bar. This repo benchmarks which prompting
strategies keep generation **on-instruction, grounded, and specific** when the
context is a real Model Development Document (MDD).

## What's measured

Each (model, technique, repetition) run produces a JSON record scored 1–5 on:

- **relevancy** — does the response address the instruction?
- **completeness** — are all required elements present?
- **specificity** — are claims tied to the supplied context?

…plus boolean error flags for **hallucination**, **redundancy**, and
**lack of specificity**. See [docs/design/evaluation-framework.md](docs/design/evaluation-framework.md).

## Headline results

Mean of relevancy/completeness/specificity, 3 reps per cell, run 2 (2025-04-16):

| model   | zero_shot | few_shot |  cot  | react |
|---------|----------:|---------:|------:|------:|
| gpt-4o  |      3.67 |   **4.11** |  3.44 |  3.78 |
| llama3  |      3.33 |     3.78 |  3.78 |  3.78 |
| qwen7b  |      3.78 |   **4.11** | **4.11** |  3.89 |

Reproduce: `python results/aggregate_run2.py`.
Full table: [results/tables/run2_mean_scores.md](results/tables/run2_mean_scores.md).

> The checked-in runs use a simulated responder so the harness is reproducible
> without API keys. With keys configured, the same runner hits the real models.

## Repo layout

```
src/mrm_prompt_bench/    # importable package
  techniques/            # one module per prompting technique
  retrieval/             # FAISS / LlamaIndex retrieval + chunking
  extraction/            # instruction extraction from .docx guidelines
  runners/               # experiment runner, prompt hub
  evaluation/            # scoring, error analysis
  io/                    # output schema + filename helpers
notebooks/               # exploratory Jupyter work (numbered 00–04)
scripts/                 # CLI entrypoints (thin wrappers over src/)
tests/                   # pytest suite
configs/                 # YAML experiment configs
data/{raw,processed,examples}/
experiments/outputs/runs/<date>_<run>/<model>/<technique>_rep<n>.json
results/{tables,figures}/
docs/{design,papers/{pdfs,notes}}/
_archive/                # superseded versions kept for reference
```

## Quickstart

```bash
git clone https://github.com/<you>/mrm-prompt-bench.git
cd mrm-prompt-bench
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env          # add OPENAI_API_KEY if running real models
pytest                        # smoke + unit tests
python results/aggregate_run2.py
```

## Reproducing an experiment

```bash
python scripts/run_experiments.py --config configs/default.yaml
python scripts/evaluate.py        --run experiments/outputs/runs/<your_run>
```

Per-run outputs land in
`experiments/outputs/runs/<YYYY-MM-DD>_<name>/<model>/<technique>_rep<n>.json`
with this schema:

```json
{
  "id": "001",
  "instruction": "...",
  "context": "...",
  "model": "gpt-4o",
  "prompting_technique": "zero_shot",
  "prompt": "...",
  "response": "...",
  "evaluation": {
    "relevancy":    {"score": 4, "rationale": "..."},
    "completeness": {"score": 4, "rationale": "..."},
    "specificity":  {"score": 2, "rationale": "..."},
    "errors": {
      "hallucination":         {"exists": false, "evidence": "", "severity": "low"},
      "redundancy":            {"exists": true,  "evidence": "...", "severity": "medium"},
      "lack_of_specificity":   {"exists": false, "evidence": "...", "severity": "high"}
    }
  },
  "generation_metadata": {"temperature": 0.3, "top_p": 0.95, "max_tokens": 600,
                          "timestamp": "2025-04-16T14:09:46Z"}
}
```

## Architecture

```
                ┌──────────────────────────┐
   guidelines → │ extraction.extract_instr │ → instructions.json
   (.docx)     └──────────────────────────┘
                              │
                              ▼
                  ┌────────────────────┐
   MDD context → │ retrieval.chunking │ ──── FAISS / LlamaIndex
                 └────────────────────┘
                              │
                              ▼
       ┌──────────────────────────────────────────┐
       │  runners.experiment_runner               │
       │  ── techniques.{zero_shot, few_shot,     │
       │      cot, react, reflexion}              │
       └──────────────────────────────────────────┘
                              │
                              ▼
              experiments/outputs/runs/<date>_<run>/
                              │
                              ▼
                  ┌────────────────────┐
                  │ evaluation         │ → results/tables, figures
                  └────────────────────┘
```

## Contributing

- Run `ruff check .` and `pytest` before opening a PR
- Keep run outputs deterministic — set `temperature: 0.0` in configs you commit
- New technique modules go under `src/mrm_prompt_bench/techniques/` with a
  matching unit test in `tests/`

See [docs/design/](docs/design/) for design notes and the experiment plan.

## License

MIT — see [LICENSE](LICENSE).
