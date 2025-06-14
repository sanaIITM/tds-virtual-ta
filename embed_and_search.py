from sentence_transformers import SentenceTransformer
import numpy as np
import json
from typing import List, Tuple

# Load a compact but good model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Store your documents and metadata
documents: List[str] = []
sources: List[Tuple[str, str]] = []  # (url, short_text)
doc_embeddings = None

def load_documents(path: str):
    global documents, sources, doc_embeddings
    with open(path, 'r') as f:
        data = json.load(f)
    documents = [item["text"] for item in data]
    sources = [(item["url"], item["text"][:80]) for item in data]
    doc_embeddings = model.encode(documents, normalize_embeddings=True)

def search(query: str, top_k: int = 3) -> List[dict]:
    global doc_embeddings
    if doc_embeddings is None:
        raise ValueError("Documents not loaded. Call load_documents() first.")
    query_vec = model.encode([query], normalize_embeddings=True)[0]
    scores = np.dot(doc_embeddings, query_vec)
    top_indices = np.argsort(scores)[-top_k:][::-1]
    results = [
        {"text": documents[i], "url": sources[i][0], "snippet": sources[i][1]}
        for i in top_indices
    ]
    return results

