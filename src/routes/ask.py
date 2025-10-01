# src/routes/ask.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List
from src.utils.retriever import Retriever
from src.utils.generator import Generator

router = APIRouter()

class AskRequest(BaseModel):
    question: str

# singletons
retriever = Retriever(index_dir="./index")
generator = Generator()

@router.post("/ask")
def ask_post(req: AskRequest):
    q = req.question
    retrieved = retriever.retrieve(q, top_k=4)
    result = generator.generate_answer(q, retrieved)
    return result

@router.get("/ask")
def ask_get(q: str = Query(..., description="Question to ask")):
    retrieved = retriever.retrieve(q, top_k=4)
    result = generator.generate_answer(q, retrieved)
    return result
