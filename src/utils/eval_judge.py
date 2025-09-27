# src/utils/eval_judge.py
def judge_answer(answer: str) -> str:
    """
    Minimal stub: simple rules-based judgment
    """
    if "I cannot answer" in answer:
        return "Fallback correctly triggered"
    elif "[" in answer and "]" in answer:
        return "Citations present"
    else:
        return "No citations found"
