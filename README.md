# AI Knowledge Assistant

A FastAPI + Streamlit app for RAG-based question answering over PDF documents with Hugging Face inference.

## Features
- Upload PDF and split into large text chunks.
- TF-IDF vector similarity search.
- Hugging Face Chat API for answers.
- Chat-style conversation flow in Streamlit.
 
### Overview
AI Knowledge Assistant is a lightweight, open-source PDF Q&A system built with:
- `Streamlit` frontend
- `FastAPI` backend
- `scikit-learn` TF-IDF vector search
- Hugging Face LLM integration (OpenAI-compatible model)

It converts PDFs into searchable “document context chunks”, then answers natural language questions using a Retrieval-Augmented Generation (RAG) flow.

---

### Why this project
- Most teams have knowledge locked in PDFs (manuals, reports, SOPs).
- This tool turns static documents into a conversational assistant.
- No expensive embedding service required—pure TF-IDF vector similarity + local store.
- Free-tier and deployment-friendly (Render + Streamlit Cloud support).

---

### Key Features
- PDF upload endpoint (`/upload`)
- Text extraction + chunking by page
- In-memory vector store with similarity search
- Stateful chat interface (history + re-ask)
- Hugging Face chat prompt + model call
- Robust deployment instructions included

---

### Architecture
1. **Upload PDF**
   - Save to uploads
   - Parse pages via `pypdf`
   - Split text into 1500-word chunks (250 overlap)
2. **Vector store**
   - `sklearn.TfidfVectorizer`
   - `cosine_similarity` query
3. **RAG answer**
   - Build prompt with top-N docs + chat history
   - Query HF `openai/gpt-oss-120b:fastest`
4. **Frontend**
   - Streamlit UI with upload, chat input, conversation display
   - `API_BASE_URL` env-configurable

---

### Tech Stack
- Python 3.14
- FastAPI
- Streamlit
- pypdf
- scikit-learn
- requests
- python-dotenv
- Hugging Face inference

---

### Deployment 
- GitHub repo → Render backend (FastAPI)
- GitHub repo → Streamlit Cloud frontend
- env vars:
  - `HUGGINGFACE_API_KEY`
  - `HUGGINGFACE_API_URL`
  - `HUGGINGFACE_API_MODEL`
  - `API_BASE_URL`

---

### Usage (quickstart)
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. `uvicorn main:app --reload`
4. `streamlit run app.py`
5. Upload PDF, ask questions

---

### Why it’s useful
- Rapid search across corporate documentation
- Quick executive summaries from PDFs
- Auto FAQ from product docs
- Training and onboarding bot prototype

---

### Next improvements
- Replace TF-IDF with embeddings (`OpenAI`, `SentenceTransformers`)
- Add per-file metadata + source ranking
- Persist vectors to disk
- Add user auth & PDF permission controls
- Add single-file multi-PDF library + tagging

---

### Call to Action
- Fork and customize with your own model & dataset.
- Share results and improvements in PRs.
- Star if this saves you time with document Q&A.

## Install
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run locally
1. Start backend: `uvicorn main:app --reload`
2. Start frontend: `streamlit run app.py`

## Environment
Create `.env`:
```
HUGGINGFACE_API_KEY=hf_xxx-your-token
HUGGINGFACE_API_URL=https://router.huggingface.co/v1/chat/completions
HUGGINGFACE_API_MODEL=openai/gpt-oss-120b:fastest
API_BASE_URL=http://localhost:8000
```

## Deploy
See deployment instructions in chat response, using Render (backend) and Streamlit Cloud (frontend).

## Author: Stanley Ekene Uzum
