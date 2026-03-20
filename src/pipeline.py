"""
src/pipeline.py

Thin orchestrator — ties retriever.py and generator.py together.
app.py only imports from here, keeping it clean.

Flow:
    build_index()       → load → chunk → embed → FAISS + save chunks.json
    get_answer_stream() → retrieve → generate (streaming)
"""

from typing import Iterator, List, Optional, Tuple

from src.retriever import (
    load_document,
    split_into_chunks,
    build_faiss_index,
    get_retriever,
    retrieve_chunks,
)
from src.generator import stream_answer


# ── Build index (called once per document) ────────────────────────────────────

def build_index(
    file_path: str,
    embed_model: str = "all-MiniLM-L6-v2",
    chunk_size: int = 800,
    chunk_overlap: int = 150,
    vectordb_dir: str = "vectordb",
    chunks_dir: str = "chunks",
) -> Tuple[object, int]:
    """
    Full ingestion pipeline:
        load → chunk (+ save JSON) → embed → FAISS index

    Returns
    -------
    (retriever, n_chunks)
    """
    docs       = load_document(file_path)
    chunks     = split_into_chunks(docs, chunk_size, chunk_overlap, chunks_dir)
    vectorstore = build_faiss_index(chunks, embed_model, vectordb_dir)
    retriever  = get_retriever(vectorstore, top_k=3)
    return retriever, len(chunks)


# ── Stream answer (called on every user query) ────────────────────────────────

def get_answer_stream(
    query: str,
    retriever,
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile",
    top_k: int = 3,
) -> Iterator[Tuple[str, Optional[List[dict]]]]:
    """
    Retrieve relevant chunks → stream LLM answer.

    Yields
    ------
    (token_str, sources_or_None)
        sources list is yielded only on the first token.
    """
    # Step 1: retrieve
    chunks = retrieve_chunks(retriever, query, top_k=top_k)

    # Step 2: stream
    first = True
    for token in stream_answer(query, chunks, groq_api_key, model_name):
        if first:
            yield token, chunks
            first = False
        else:
            yield token, None