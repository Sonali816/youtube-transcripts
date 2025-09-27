# src/main.py

import argparse
from fastapi import FastAPI
import uvicorn
from src.routes.ask import router, retriever, generator

app = FastAPI()
app.include_router(router)

print("[Main] App initialized and router included.")

def cli_query(q):
    retrieved = retriever.retrieve(q, top_k=4)
    if not retrieved:
        print("I cannot answer from the provided transcripts.")
        return
    ans = generator.generate_answer(q, retrieved)
    print("\n=== Answer ===\n")
    print(ans["answer"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=str, help="Question to ask")
    parser.add_argument("--serve", action="store_true", help="Run API server")
    args = parser.parse_args()
    if args.serve:
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=False)
    elif args.q:
        cli_query(args.q)
    else:
        print("Run with --q 'question' or --serve to run API.")
