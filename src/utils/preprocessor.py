import re
from pathlib import Path

def load_transcript(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8")

def normalize_transcript(raw_text: str) -> str:
    text = raw_text
    text = re.sub(r"^WEBVTT.*\n", "", text)
    text = re.sub(r"^\d+\n", "", text, flags=re.MULTILINE)
    text = re.sub(
        r"(\d{2}:\d{2}:\d{2})\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}",
        r"[\1]",
        text,
    )
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def preprocess_file(file_path: str) -> str:
    raw = load_transcript(file_path)
    return normalize_transcript(raw)
