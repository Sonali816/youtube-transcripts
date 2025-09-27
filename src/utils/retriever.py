from .embed import EmbeddingStore

class Retriever:
    def __init__(self, model_name="all-MiniLM-L6-v2", index_dir="./index"):
        self.store = EmbeddingStore(model_name=model_name, index_dir=index_dir)

    def retrieve(self, query, top_k=3):
        query_embedding = self.store.model.encode(query).tolist()

        results = self.store.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        hits = []
        for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
            hits.append({
                "text": doc,
                "source": meta.get("source", "unknown"),
                "start": meta.get("start", "00:00:00"),
                "end": meta.get("end", "00:00:00")
            })
        #print(hits.__len__)
        return hits
