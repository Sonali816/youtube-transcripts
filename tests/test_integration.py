from src.routes.ask import retriever, generator

def test_end_to_end_example():
    q = "How should I make my introductions hook viewers?"
    retrieved = retriever.retrieve(q, top_k=4)
    ans = generator.generate_answer(q, retrieved)
    
    assert isinstance(ans, dict)
    assert "answer" in ans and isinstance(ans["answer"], str) and len(ans["answer"]) > 0
