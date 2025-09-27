# src/utils/eval_bertscore.py
def compute_bertscore(pred: str, reference: str) -> float:
    """
    Minimal stub: returns dummy score.
    Replace with real BERTScore if desired.
    """
    return 1.0 if pred.strip() == reference.strip() else 0.5
