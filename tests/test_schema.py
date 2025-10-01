import re
from src.routes.ask import router, retriever, generator

CITATION_RE = re.compile(r"\[source:\s*.+? t=\d{2}:\d{2}:\d{2}–\d{2}:\d{2}:\d{2}\]")

def test_citation_format():
    # craft a fake generated answer that includes a citation
    s = "Do X. [source: aprilynne.txt t=00:12:34–00:13:10]"
    assert CITATION_RE.search(s)
