from src.routes.ask import retriever
import pytest

def test_grounding_to_hayden():
    q = "How can I improve storytelling in my videos?"
    retrieved = retriever.retrieve(q, top_k=5)
    print("Retrieved passages:", retrieved)  # Debug output
    assert any("hayden" in r["source"].lower() for r in retrieved), "No hayden citations found in retrieval"
