# Transcript-Grounded YouTube Advisor

A small, production-minded chatbot that gives creators practical, transcript-grounded advice using only two provided transcripts.

## What’s included

* **FastAPI endpoint**: `POST /ask` that returns grounded advice with citations.
* **CLI**: `python src/main.py --q "How do I improve storytelling?"`
* **Ingestion script** to preprocess transcripts and build a ChromaDb vector index.
* **Simple RAG generator** using local free models.
* **Tests** (pytest) and a minimal eval harness.

## Quick setup (Linux/Mac)

1. Clone or create the project directory and place the provided `transcripts/` folder with `aprilynne.txt` and `hayden.txt`.

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run ingestion to build the index:

   ```bash
   python scripts/ingestion_script.py \
     --transcripts_dir transcripts \
     --index_dir ./index \
     --chunk_size 300 \
     --overlap 50
   ```

   This will create an `index/` directory containing the ChromaDB index and metadata.

4. Start the API server:

   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

   Example query:

   ```bash
   curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question":"How do I improve video intros?"}'
   ```

   Example output:

   ```json
   {
     "answer": "Provide 3–5 short, actionable recommendations tailored to the question, each followed immediately by one or more CITATIONs in the format: [source: filename> t=MM:SS–MM:SS]. For each recommendation, include a one-sentence rationale grounded in the PASSAGEs.",
     "citations": ["filename> t=MM:SS–MM:SS"]
   }
   ```

5. CLI usage:

   ```bash
   python src/main.py --q "How can I improve my thumbnails and CTR?"
   ```

## Tests

Run:

```bash
pytest -q
```
