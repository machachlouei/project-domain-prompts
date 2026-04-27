"""CLI entrypoint for running prompting-technique experiments.

Thin wrapper over `mrm_prompt_bench.runners.experiment_runner`.
"""

from mrm_prompt_bench.runners import experiment_runner


if __name__ == "__main__":
    experiment_runner.main()  # type: ignore[attr-defined]
