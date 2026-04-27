"""CLI entrypoint for extracting guideline instructions from .docx sources.

Thin wrapper over `mrm_prompt_bench.extraction.extract_instructions`.
"""

from mrm_prompt_bench.extraction import extract_instructions


if __name__ == "__main__":
    extract_instructions.main() if hasattr(extract_instructions, "main") else None
