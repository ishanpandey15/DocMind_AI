"""
src/generator.py

Handles:
    5. Prompt construction  (system + context + user query)
    6. LLM streaming        (Groq via LangChain ChatGroq)

The generator is intentionally kept separate from the retriever
so each component can be tested and swapped independently.
"""

from typing import Iterator, List, Optional, Tuple

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ── Prompt template ───────────────────────────────────────────────────────────

SYSTEM_MSG = """You are DocMind, a precise and helpful document assistant.
Answer the user's question using ONLY the context excerpts provided below.
If the answer is not present in the context, clearly say:
"I couldn't find that information in the provided document."
Never fabricate facts. Be clear, concise, and use bullet points for multi-part answers."""

PROMPT = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_MSG),
    ("human", """Context excerpts from the document:
{context}

---
Question: {question}

Answer strictly based on the context above:"""),
])


# ── Context builder ───────────────────────────────────────────────────────────

def build_context(chunks: List[dict]) -> str:
    """
    Join retrieved chunks into a single context string for the prompt.
    Each chunk is labelled with its ID for traceability.
    """
    parts = []
    for c in chunks:
        parts.append(f"[Chunk #{c['id']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)


# ── Streaming generator ───────────────────────────────────────────────────────

def stream_answer(
    query: str,
    chunks: List[dict],
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile",
    temperature: float = 0.0,
    max_tokens: int = 1024,
) -> Iterator[str]:
    """
    Build a prompt from retrieved chunks + query, then stream the
    LLM response token-by-token via Groq.

    Parameters
    ----------
    query         : user's natural language question
    chunks        : list of retrieved chunk dicts (from retriever.retrieve_chunks)
    groq_api_key  : Groq API key
    model_name    : Groq model to use
    temperature   : 0 = deterministic (recommended for factual QA)
    max_tokens    : max tokens in the generated response

    Yields
    ------
    str : one token / small chunk of text at a time
    """
    llm = ChatGroq(
        api_key=groq_api_key,
        model_name=model_name,
        streaming=True,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    context = build_context(chunks)
    chain   = PROMPT | llm | StrOutputParser()

    print(f"[Generator] Streaming with '{model_name}' | context chunks: {len(chunks)}")
    for token in chain.stream({"context": context, "question": query}):
        yield token


def generate_answer(
    query: str,
    chunks: List[dict],
    groq_api_key: str,
    model_name: str = "llama-3.3-70b-versatile",
) -> str:
    """
    Non-streaming version — returns the full answer as a single string.
    Useful for batch evaluation (RAGAS notebook).
    """
    return "".join(stream_answer(query, chunks, groq_api_key, model_name))