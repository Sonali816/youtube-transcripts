from src.utils.retriever import Retriever

# Initialize retriever (make sure index_dir matches ingestion)
retriever = Retriever(index_dir="./index")

# Test query
query = "How do I improve video intros?"

# Retrieve top 4 matching chunks
hits = retriever.retrieve(query, top_k=4)

if not hits:
    print("No relevant passages found.")
else:
    print("Retrieved passages:")
    for h in hits:
        print(f"- [{h['source']} {h['start']}–{h['end']}] {h['text'][:100]}...")
