# Mean evaluation scores — 2025-04-16 run 2

Mean of (relevancy + completeness + specificity) / 3, scored 1–5,
across 3 repetitions per (model, technique) pair.

| model   | zero_shot | few_shot | cot   | react |
|---------|----------:|---------:|------:|------:|
| gpt-4o  |      3.67 |     4.11 |  3.44 |  3.78 |
| llama3  |      3.33 |     3.78 |  3.78 |  3.78 |
| qwen7b  |      3.78 |     4.11 |  4.11 |  3.89 |

Source: `experiments/outputs/runs/2025-04-16_run2/<model>/<technique>_rep{1,2,3}.json`.
Reproduce with `python results/aggregate_run2.py`.

> **Note.** Responses in these checked-in runs were simulated, not real model
> calls — they exercise the harness end-to-end. Real-model runs will overwrite
> this table when reproduced with API keys configured.
