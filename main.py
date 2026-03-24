import os
import shutil
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

vector_db = None


class AskRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = None


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    from document_loader import load_and_split
    from vector_store import create_vector_store

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    docs = load_and_split(file_path)

    global vector_db
    vector_db = create_vector_store(docs)

    return {"message": "File uploaded and processed"}


@app.post("/ask")
def ask(body: AskRequest):
    from rag import generate_answer

    if vector_db is None:
        return {"answer": "Upload a document first."}

    try:
        answer = generate_answer(vector_db, body.question, history=body.history)
    except Exception as e:
        return {"answer": f"Error generating answer: {e}."}

    return {"answer": answer}
