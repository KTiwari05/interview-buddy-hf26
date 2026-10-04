import os
import time
from typing import Literal

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

app = FastAPI(title="Interview Buddy")
OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")

PROMPTS = {
    "explain": "Explain the concept clearly. Define unfamiliar terms, then give one concrete takeaway.",
    "simpler": "Explain using a familiar everyday analogy, then connect it to the technical concept. Avoid jargon.",
    "example": "Give one small practical example. For code, use Java or SQL, put it in a fenced code block, and explain how it works.",
    "interview": "Give a concise answer someone could say in a software engineering interview. Include an important tradeoff when relevant.",
}


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    mode: Literal["explain", "simpler", "example", "interview"] = "explain"

    @field_validator("question")
    @classmethod
    def strip_question(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Enter a question.")
        return value


@app.get("/health")
async def health():
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{OLLAMA_URL}/api/tags")
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(503, "Open Ollama and try again.") from exc
    if MODEL not in [model["name"] for model in response.json()["models"]]:
        raise HTTPException(503, f"Download the model with: ollama pull {MODEL}")
    return {"status": "ready", "model": MODEL}


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    started = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=300) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",
                json={
                    "model": MODEL,
                    "stream": False,
                    "think": False,
                    "messages": [
                        {"role": "system", "content": "Help a developer rehearse medium-difficulty Java backend interviews. "
                         + PROMPTS[request.mode] + " Answer directly in at most 120 words using Markdown. "
                         "Do not include planning, a word count, or invented personal experience. Say if uncertain."},
                        {"role": "user", "content": request.question + "\n/no_think"},
                    ],
                    "options": {"temperature": 0.3, "num_predict": 1024, "num_ctx": 2048},
                },
            )
            response.raise_for_status()
    except httpx.TimeoutException as exc:
        raise HTTPException(504, "The local model took too long. Try a shorter question.") from exc
    except httpx.HTTPError as exc:
        raise HTTPException(503, "Could not reach the local model. Check that Ollama is running and the model is downloaded.") from exc
    result = response.json()
    if result.get("done_reason") == "length":
        raise HTTPException(502, "The model reached its answer limit. Ask a more specific question.")
    # Qwen can include a reasoning prefix even with thinking disabled.
    answer = result["message"]["content"].split("</think>", 1)[-1].strip()
    if not answer:
        raise HTTPException(502, "The model returned an empty answer. Try again.")
    return {"answer": answer, "model": MODEL, "seconds": round(time.perf_counter() - started, 2)}
