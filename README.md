# AI Knowledge Assistant

A FastAPI + Streamlit app for RAG-based question answering over PDF documents with Hugging Face inference.

## Features
- Upload PDF and split into large text chunks.
- TF-IDF vector similarity search.
- Hugging Face Chat API for answers.
- Chat-style conversation flow in Streamlit.

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
