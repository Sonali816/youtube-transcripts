# src/utils/generator.py

import requests
from typing import List, Dict
import re

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"  # Run `ollama run llama3` before using

class Generator:
    def __init__(self, model_name=OLLAMA_MODEL):
        self.model_name = model_name
        print(f"[Generator] Using Ollama model: {self.model_name}")

    def generate_answer(self, question: str, retrieved: List[dict]) -> Dict:
        print(f"[generate_answer] Received question: {question}")
        if not retrieved:
            print("[generate_answer] No retrieved passages found.")
            return {"answer": "I cannot answer from the provided transcripts.", "citations": []}

        passages = ""
        for i, r in enumerate(retrieved):
            start = r.get("start") or "??:??:??"
            end = r.get("end") or "??:??:??"
            source = r.get("source") or "unknown"
            text = r.get("text", "").replace("\n", " ").strip()
            cid = f"[source: {source} t={start}–{end}]"
            passages += f"PASSAGE {i+1}:\n{text}\nCITATION: {cid}\n\n"
            print(f"[generate_answer] Added passage {i+1} with citation {cid}")

        prompt = f"""
You are an assistant. Based only on the passages below, answer the question.

Question: {question}

PASSAGES:
{passages}

Instructions:
- Write 3–5 short actionable recommendations.
- After each, include the provided citation exactly as shown: [source: <filename> t=MM:SS–MM:SS].
- If you cannot answer from the passages, respond exactly: "I cannot answer from the provided transcripts."

Answer:
""".strip()

        print(f"[generate_answer] Prompt length: {len(prompt)} characters")

        response = requests.post(OLLAMA_URL, json={
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        })

        if response.status_code != 200:
            print(f"[generate_answer] Error from Ollama: {response.status_code} - {response.text}")
            return {"answer": "Error generating answer.", "citations": []}

        answer = response.json().get("response", "").strip()
        print(f"[generate_answer] Generated answer:\n{answer}")

        citations_raw = re.findall(r"\[source:\s*([^\]]+)\]", answer)
        citations = list(set(citations_raw))
        print(f"[generate_answer] Extracted citations: {citations}")

        return {"answer": answer, "citations": citations}
    
if __name__ == "__main__":
    generator = Generator()
    question = "How do I improve video intros?"
    # Simulate retrieved passages — example data format:
    retrieved = [
        {
            "start": "00:00:10",
            "end": "00:00:20",
            "source": "transcripts/sample.txt",
            "text": "To improve your video intros, keep them short and engaging."
        }
    ]
    result = generator.generate_answer(question, retrieved)
    print("\nGenerated Answer:\n", result["answer"])
    print("\nExtracted Citations:\n", result["citations"])

