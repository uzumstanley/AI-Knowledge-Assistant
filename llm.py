import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_NAME = os.getenv("HUGGINGFACE_API_MODEL", "openai/gpt-oss-120b:fastest")
HUGGINGFACE_API_URL = os.getenv("HUGGINGFACE_API_URL", "https://router.huggingface.co/v1/chat/completions")

print(f"[llm] MODEL_NAME={MODEL_NAME}")
print(f"[llm] API_KEY set={bool(API_KEY)}")
print(f"[llm] HUGGINGFACE_API_URL={HUGGINGFACE_API_URL}")


def _extract_content(data):
    if not isinstance(data, dict):
        return None

    choices = data.get("choices")
    if not choices or not isinstance(choices, list):
        return None

    first = choices[0]
    message = first.get("message")

    if isinstance(message, dict):
        content = message.get("content")
        if content and isinstance(content, str) and content.strip():
            return content.strip()

        reasoning = message.get("reasoning")
        if reasoning and isinstance(reasoning, str) and reasoning.strip():
            return reasoning.strip()

    text = first.get("text")
    if text and isinstance(text, str) and text.strip():
        return text.strip()

    return None


def query_llm(prompt: str, max_tokens: int = 512):
    if not API_KEY:
        return "(No API key set) " + prompt[:300]

    api_url = HUGGINGFACE_API_URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }

    resp = requests.post(api_url, headers=headers, json=payload, timeout=120)

    if resp.status_code in (401, 403):
        return f"(API token invalid or unauthorized: HTTP {resp.status_code})"

    if resp.status_code != 200:
        raise RuntimeError(f"LLM error: HTTP {resp.status_code} {resp.text}")

    try:
        data = resp.json()
    except ValueError:
        raise RuntimeError(f"LLM error: invalid JSON from API: {resp.text}")

    content = _extract_content(data)
    if content is not None:
        return content

    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(f"LLM error: {data.get('error')}")

    return str(data)


