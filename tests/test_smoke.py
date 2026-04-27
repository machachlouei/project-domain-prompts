"""Smoke tests: confirm the package and its submodules are importable."""

import importlib

MODULES = [
    "mrm_prompt_bench",
    "mrm_prompt_bench.techniques",
    "mrm_prompt_bench.retrieval",
    "mrm_prompt_bench.extraction",
    "mrm_prompt_bench.runners",
    "mrm_prompt_bench.evaluation",
    "mrm_prompt_bench.io",
]


def test_package_imports():
    for name in MODULES:
        importlib.import_module(name)
