import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Knowledge Assistant")
st.title("🧠 AI Knowledge Assistant")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    try:
        requests.post(f"{API_BASE_URL}/upload", files=files)
        st.success("Uploaded successfully!")
    except Exception as e:
        st.error(f"Upload failed: {e}")

if "history" not in st.session_state:
    st.session_state.history = []

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question"):
    st.session_state.history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "question": prompt,
            "history": st.session_state.history[:-1],
        }

        res = requests.post(
            f"{API_BASE_URL}/ask",
            json=payload,
            timeout=60,
        )

        if res.status_code != 200:
            answer = f"Error: {res.status_code} {res.text}"
        else:
            answer = res.json().get("answer", "No answer received.")

        st.session_state.history.append({"role": "assistant", "content": answer})

        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        error_msg = f"Request failed: {e}"
        st.session_state.history.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.markdown(error_msg)

