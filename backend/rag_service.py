import os
from typing import List, Optional

import numpy as np
from sqlalchemy.orm import Session
from openai import OpenAI
import google.generativeai as genai

from models import AcademicSource


EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_EMBED_MODEL = os.getenv(
    "GEMINI_EMBED_MODEL", "models/text-embedding-004")
TARGET_VECTOR_DIM = 1536


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_gemini_client():
    if not GEMINI_API_KEY:
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    return genai


def _pad_or_trim(vec: List[float], size: int) -> List[float]:
    if len(vec) == size:
        return vec
    if len(vec) > size:
        return vec[:size]
    return vec + [0.0] * (size - len(vec))


def embed_texts(texts: List[str]) -> List[List[float]]:
    if not texts:
        return []
    # Prefer Gemini if key provided; otherwise use OpenAI
    if GEMINI_API_KEY:
        print(f"Using Gemini with model: {GEMINI_EMBED_MODEL}")
        client = get_gemini_client()
        embeddings = []
        for i, t in enumerate(texts):
            try:
                print(f"Embedding text {i+1}/{len(texts)}: {t[:50]}...")
                r = client.embed_content(model=GEMINI_EMBED_MODEL, content=t)
                print(f"Response type: {type(r)}")
                print(
                    f"Response keys: {r.keys() if hasattr(r, 'keys') else 'No keys'}")
                # Try different response formats
                if hasattr(r, 'embedding') and hasattr(r.embedding, 'values'):
                    vec = r.embedding.values
                elif isinstance(r, dict) and 'embedding' in r:
                    # Handle direct embedding array format
                    if isinstance(r['embedding'], list):
                        vec = r['embedding']
                    elif 'values' in r['embedding']:
                        vec = r['embedding']['values']
                    else:
                        print(f"Unexpected embedding format: {r['embedding']}")
                        raise ValueError(f"Unexpected embedding format: {type(r['embedding'])}")
                else:
                    print(f"Unexpected response format: {r}")
                    raise ValueError(f"Unexpected response format: {type(r)}")
                print(f"Vector length: {len(vec)}")
                embeddings.append(_pad_or_trim(vec, TARGET_VECTOR_DIM))
            except Exception as e:
                print(f"Error embedding text {i+1}: {type(e).__name__}: {e}")
                raise
        return embeddings
    else:
        client = get_openai_client()
        resp = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
        return [item.embedding for item in resp.data]


def build_source_text(source: AcademicSource) -> str:
    parts = [source.title or "", source.authors or "",
             source.abstract or "", source.full_text or ""]
    return "\n\n".join([p for p in parts if p])


def ingest_missing_embeddings(db: Session) -> int:
    """Generate embeddings for sources missing vector and store them in DB."""
    sources = db.query(AcademicSource).filter(AcademicSource.embedding == None).all()  # noqa: E711
    if not sources:
        return 0
    payloads = [build_source_text(s) for s in sources]
    vectors = embed_texts(payloads)
    for src, vec in zip(sources, vectors):
        src.embedding = vec
    db.commit()
    return len(sources)


def vector_search(db: Session, query: str, limit: int = 5) -> List[AcademicSource]:
    """Return top-k sources by cosine similarity using pgvector."""
    [q_vec] = embed_texts([query])
    # ORDER BY embedding <=> q_vec uses L2 distance by default; for cosine, use vector_cosine_ops index.
    return (
        db.query(AcademicSource)
        .order_by(AcademicSource.embedding.cosine_distance(q_vec))
        .limit(limit)
        .all()
    )
