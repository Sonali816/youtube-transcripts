import re
from typing import List, Dict

def parse_timestamps_from_segment(seg_text: str):
    timestamps = re.findall(r"\[(\d{2}:\d{2}:\d{2})\]", seg_text)
    if timestamps:
        return timestamps[0], timestamps[-1]
    return None, None

def split_into_sentences(text: str) -> List[str]:
    return re.split(r'(?<=[.!?])\s+', text.strip())

def chunk_transcript(
    normalized_text: str,
    chunk_size: int = 300,
    overlap: int = 50,
    source_filename: str = "transcript.txt"
) -> List[Dict]:
    sentences = split_into_sentences(normalized_text)
    chunks = []
    cur_chunk = ""
    i = 0
    j = 0

    while j < len(sentences):
        while len(cur_chunk) < chunk_size and j < len(sentences):
            if cur_chunk:
                cur_chunk += " "
            cur_chunk += sentences[j]
            j += 1

        start_ts, end_ts = parse_timestamps_from_segment(cur_chunk)
        chunks.append({
            "id": f"{source_filename}_{i}",
            "text": cur_chunk,
            "source": source_filename,
            "start_ts": start_ts or "00:00:00",
            "end_ts": end_ts or "00:00:00"
        })
        i += 1

        if overlap > 0:
            cur_chunk = cur_chunk[max(0, len(cur_chunk) - overlap):]
        else:
            cur_chunk = ""

    if cur_chunk.strip():
        start_ts, end_ts = parse_timestamps_from_segment(cur_chunk)
        chunks.append({
            "id": f"{source_filename}_{i}",
            "text": cur_chunk,
            "source": source_filename,
            "start_ts": start_ts or "00:00:00",
            "end_ts": end_ts or "00:00:00"
        })

    return chunks, None
