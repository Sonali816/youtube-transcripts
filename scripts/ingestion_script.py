import glob
import os
from src.utils.preprocessor import preprocess_file
from src.utils.chunk import chunk_transcript
from src.utils.embed import EmbeddingStore

def ingest():
    # Use absolute path to avoid directory mismatches
    index_dir = os.path.abspath("./index")
    print(f"Using index directory: {index_dir}")

    store = EmbeddingStore(
        index_dir=index_dir,
        model_name="all-MiniLM-L6-v2",
        collection_name="youtube_advisor"
    )

    all_files = glob.glob("transcripts/*.txt")
    print("Found transcript files:", all_files)

    for fpath in all_files:
        print(f"\nProcessing {fpath}...")
        normalized_text = preprocess_file(fpath)
        chunks, _ = chunk_transcript(normalized_text, source_filename=fpath)
        
        print(f"Number of chunks for {fpath}: {len(chunks)}")
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks as sample
            print(f"Sample chunk {i}: {chunk['text'][:100]}...")  # print first 100 chars

        # Filter out empty chunks just in case
        chunks_to_add = [c for c in chunks if c["text"].strip()]
        if not chunks_to_add:
            print(f"No valid chunks found for {fpath}, skipping...")
            continue

        # Embed and store chunks
        store.embed_chunks(chunks_to_add)

    print("\nIngestion completed. Embeddings saved to Chroma.")

if __name__ == "__main__":
    ingest()
