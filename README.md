# DocMind AI - RAG Chatbot (LangChain + Groq + FAISS)

A production-quality Retrieval-Augmented Generation chatbot that answers questions about any PDF or text document. Built with LangChain, Groq LLM (free, ultra-fast), and FAISS vector database, served through a Streamlit interface with real-time streaming.

---

## Architecture

```
User Query
    |
    v
Streamlit UI (app.py)
Dark theme · Token streaming · Source chips
    |
    v
RAG Pipeline (src/pipeline.py)

[1] PDFPlumberLoader / TextLoader  ->  raw document text
[2] RecursiveCharacterTextSplitter ->  ~800 char chunks (150 overlap)
[3] HuggingFaceEmbeddings          ->  384-dim dense vectors
[4] FAISS.from_documents           ->  saved cosine-similarity index
[5] retriever.invoke(query)        ->  top-K relevant chunks
[6] ChatGroq (streaming=True)      ->  token-by-token answer
```

---

## Folder Structure

```
docmind_ai/
├── app.py                  # Streamlit chatbot UI
├── requirements.txt
├── README.md
├── data/                   # Uploaded documents , Also documents can be uploaded from the frontend
├── vectordb/               # FAISS index
├── notebooks/
│   └── rag_notebook.ipynb
└── src/
    ├── __init__.py
    └── pipeline.py         # Full LangChain RAG pipeline
```


---

## Quick Setup

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/docmind-ai.git
cd docmind-ai

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Get a free Groq API key

Go to https://console.groq.com, sign up (free), create an API key.

### 3. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## How to Use

1. Sidebar: Upload your PDF or .txt file
2. Paste your Groq API key in the sidebar
3. Choose model, embedding model, chunk settings
4. Click "Build Index" - document gets chunked, embedded, stored in FAISS
5. Once status shows READY, type your question and hit Send
6. Watch the response stream token-by-token
7. Expand source chunks to see which passages grounded the answer

---

## Model and Tech Choices

### LLM: Groq (llama3-8b-8192)
- Groq runs LLaMA 3 on custom LPU hardware -> ~500 tokens/sec
- Free tier available, no credit card needed
- streaming=True in LangChain ChatGroq enables real-time token streaming
- Alternative: mixtral-8x7b-32768 for longer context documents (32K tokens)

### Embeddings: all-MiniLM-L6-v2
- 22M parameters, 384-dim output, runs locally on CPU
- normalize_embeddings=True gives cosine similarity via dot product
- Source: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

### Vector DB: FAISS
- FAISS.from_documents() handles embed + index in one call
- vectorstore.save_local() persists the index between sessions
- Source: https://faiss.ai / LangChain FAISS docs

### Chunking: RecursiveCharacterTextSplitter
- Splits on paragraph breaks first, then sentences, then words
- chunk_overlap=150 carries context across chunk boundaries
- Source: LangChain text splitters documentation

---

## Prompt Format

```
System:
  You are DocMind, a helpful document assistant.
  Answer using ONLY the provided context.
  If not in context, say so. Never fabricate.