from src.routes.ask import retriever, generator

def test_fallback_out_of_scope():
    # A question unlikely to be in transcripts
    q = "What is the capital of France?"
    
    # Retrieve top 3 passages (can be empty or unrelated)
    retrieved = retriever.retrieve(q, top_k=3)
    
    # Generate answer
    ans = generator.generate_answer(q, retrieved)
    
    # Access the actual answer string (if ans is a dict)
    answer_text = ans["answer"] if isinstance(ans, dict) else ans

    # Assert fallback behavior
    assert "i cannot answer from the provided transcripts" in answer_text.lower()
