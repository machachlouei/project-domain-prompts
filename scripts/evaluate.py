"""CLI entrypoint for evaluating experiment outputs.

Thin wrapper over `mrm_prompt_bench.evaluation.evaluation`.
"""

from mrm_prompt_bench.evaluation import evaluation


if __name__ == "__main__":
    evaluation.main() if hasattr(evaluation, "main") else None
