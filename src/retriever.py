"""
src/retriever.py

Handles:
    1. Document loading  (PDF / TXT)
    2. Chunking          (RecursiveCharacterTextSplitter)
    3. Embedding         (HuggingFaceEmbeddings)
    4. FAISS index       (build + save + load)
    5. Semantic search   (retrieve top-K chunks)

Chunks are also saved to chunks/chunks.json so the folder is not empty
and can be inspected / used for evaluation.
"""

import json
from pathlib import Path
from typing import List, Tuple

from langchain_community.document_loaders import PDFPlumberLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings


# ── Document loader ───────────────────────────────────────────────────────────

def load_document(file_path: str) -> list:
    """Load a PDF or TXT file and return a list of LangChain Documents."""
    print(f"[Retriever] Loading: {file_path}")
    if file_path.lower().endswith(".pdf"):
        loader = PDFPlumberLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    print(f"[Retriever] Loaded {len(docs)} page(s)")
    return docs


# ── Chunker ───────────────────────────────────────────────────────────────────

def split_into_chunks(
    docs: list,
    chunk_size: int = 800,
    chunk_overlap: int = 100,
    chunks_dir: str = "chunks",
) -> list:
    """
    Split documents into overlapping chunks using sentence-aware splitting.
    Also saves chunks to chunks/chunks.json for inspection.

    Separator priority (highest → lowest):
        \\n\\n  paragraph breaks
        \\n     line breaks
        . ! ?  sentence endings
        space  word boundary (last resort)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " ", ""],
    )
    chunks = splitter.split_documents(docs)
    print(f"[Retriever] Created {len(chunks)} chunks")

    # ── Save chunks to chunks/chunks.json ─────────────────────────────────
    out_dir = Path(chunks_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    serializable = [
        {
            "id":     i,
            "text":   c.page_content,
            "source": c.metadata.get("source", "unknown"),
            "page":   c.metadata.get("page", "—"),
            "n_chars": len(c.page_content),
        }
        for i, c in enumerate(chunks)
    ]

    out_path = out_dir / "chunks.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

    print(f"[Retriever] Chunks saved to '{out_path}'")
    return chunks


# ── Embedder + FAISS ──────────────────────────────────────────────────────────

def build_faiss_index(
    chunks: list,
    embed_model: str = "all-MiniLM-L6-v2",
    vectordb_dir: str = "vectordb",
) -> FAISS:
    """
    Generate embeddings for all chunks and build a FAISS vector index.

    Uses normalize_embeddings=True so cosine similarity = dot product,
    which FAISS computes efficiently via IndexFlatIP.
    """
    print(f"[Retriever] Embedding with '{embed_model}'…")
    embeddings = HuggingFaceEmbeddings(
        model_name=embed_model,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(vectordb_dir)
    print(f"[Retriever] FAISS index saved to '{vectordb_dir}'")
    return vectorstore


def get_retriever(vectorstore: FAISS, top_k: int = 3):
    """Return a LangChain retriever from an existing FAISS vectorstore."""
    return vectorstore.as_retriever(search_kwargs={"k": top_k})


# ── Semantic search ───────────────────────────────────────────────────────────

def retrieve_chunks(retriever, query: str, top_k: int = 3) -> List[dict]:
    """
    Search the FAISS index for the most relevant chunks.

    Returns a list of dicts: {id, text, source, page}
    """
    retriever.search_kwargs["k"] = top_k
    source_docs = retriever.invoke(query)

    return [
        {
            "id":     i,
            "text":   doc.page_content,
            "source": doc.metadata.get("source", "—"),
            "page":   doc.metadata.get("page", "—"),
        }
        for i, doc in enumerate(source_docs)
    ]