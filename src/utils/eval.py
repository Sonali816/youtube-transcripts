# src/utils/eval.py

from src.routes.ask import retriever, generator
from src.utils.eval_generation import check_generation_format
from src.utils.eval_judge import judge_answer
from src.utils.eval_bertscore import compute_bertscore  # currently dummy
from pprint import pprint

PROMPTS = [
    ("Storytelling improvements", "How can I improve storytelling in my videos?", "Use personal stories and narrative arcs."),
    ("Introductions", "How should I structure my video introductions to retain viewers?", "Start with a hook and preview what’s coming."),
    ("Out of scope", "What is the population of Tokyo?", "I cannot answer from the provided transcripts.")
]

def run_eval():
    for name, q, reference in PROMPTS:
        print(f"\n=== {name} ===")
        print(f"Q: {q}")

        # Retrieve top passages
        retrieved = retriever.retrieve(q, top_k=4)
        passages = [f'{r["source"]}({r.get("start", "??:??:??")}-{r.get("end", "??:??:??")})' for r in retrieved]
        print("Retrieved:", passages)

        # Generate answer
        output = generator.generate_answer(q, retrieved)
        answer = output["answer"] if isinstance(output, dict) else output
        print("Answer:\n", answer)

        # Eval 1: Format check
        format_ok = check_generation_format(answer)
        print("✓ Format valid?:", format_ok)

        # Eval 2: Judgment (fallback, citations, etc.)
        judgment = judge_answer(answer)
        print("✓ Judgment:", judgment)

        # Eval 3: BERTScore (only meaningful if using real scoring logic)
        ber_score = compute_bertscore(answer, reference)
        print("✓ BERTScore (stub):", ber_score)

        print("\n" + "=" * 60)

if __name__ == "__main__":
    run_eval()
