import chromadb
from sentence_transformers import SentenceTransformer

class EmbeddingStore:
    def __init__(self, index_dir="./index", model_name="all-MiniLM-L6-v2", collection_name="youtube_advisor"):
        self.index_dir = index_dir
        self.model = SentenceTransformer(model_name)

        # Use PersistentClient instead of plain Client
        self.client = chromadb.PersistentClient(path=index_dir)

        # Get or create collection
        if collection_name in [c.name for c in self.client.list_collections()]:
            self.collection = self.client.get_collection(name=collection_name)
        else:
            self.collection = self.client.create_collection(name=collection_name)

    def embed_chunks(self, chunks):
        """
        Embed transcript chunks and store them in ChromaDB.
        Each chunk is a dict with keys: {"text", "source", "start_ts", "end_ts"}.
        """
        for chunk in chunks:
            doc_id = f"{chunk['source']}_{chunk['start_ts']}_{chunk['end_ts']}"

            # Check for duplicates
            existing = self.collection.get(ids=[doc_id])
            if existing and existing.get("ids"):
                print(f"Skipping duplicate: {doc_id}")
                continue

            embedding = self.model.encode(chunk["text"]).tolist()

            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[{
                    "source": chunk["source"],
                    "start": chunk["start_ts"],
                    "end": chunk["end_ts"]
                }]
            )
            print(f"Added: {doc_id}")
