# src/utils/eval_generation.py
def check_generation_format(answer: str) -> bool:
    """
    Minimal check: ensure answer is a non-empty string with at least one bullet point.
    """
    return bool(answer.strip()) and ("-" in answer or "\n" in answer)
