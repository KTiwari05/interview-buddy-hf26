# Interview Buddy

A small local study companion: ask one Java backend interview question, then explore a
clear explanation, a simpler analogy, a practical example, and an interview answer.

Built October 4, 2026 for the Hacktoberfest Weekend Challenge. Product direction
comes from recent Indian developer discussions; see [research notes](submission/RESEARCH.md).
Built for the author's friend Raj, who is preparing for Java backend developer interviews,
with medium difficulty practice as the target. The current scope is backend concept
refreshers, not a complete Java backend interview curriculum. Raj's testing and feedback
are pending. The separate Reddit research profile is a composite.

## Run locally

Requirements: Python 3.11 or later, [uv](https://docs.astral.sh/uv/), Node.js
22.12 or later, and [Ollama](https://ollama.com/). Download the model first:

```powershell
ollama pull qwen3:4b
```

Keep Ollama running. In one terminal, from this repository:

```powershell
cd backend
uv sync --locked
uv run uvicorn main:app --host 127.0.0.1 --port 8000
```

In a second terminal, from this repository:

```powershell
cd frontend
npm ci
npm run dev
```

Open http://127.0.0.1:5173. Backend API docs: http://127.0.0.1:8000/docs.
Choose a starter question or enter your own, select a mode, then ask. Once an answer
appears, selecting another mode generates another view of the same question.
Switching starter topics resets the answer. Read the answer, look away, and explain
the idea in your own words.

Practice starts at medium difficulty. Starters cover database indexes, Spring Boot
constructor injection, database tradeoffs, Java HashMap, and project decisions.
Code examples default to Java or SQL; Explain simpler gives an analogy when needed.

The model is configurable through `OLLAMA_MODEL` in the backend environment. The
prompts and reasoning-prefix handling are designed and tested with Qwen3 4B;
alternative models are not verified.

## Architecture

```text
React + Vite  -- /api/ask (local proxy) --> FastAPI
                                               |
                                    Ollama /api/chat
                                               |
                                           Qwen3 4B
```

There is no database, account, retrieval service, or paid model API. The app sends
questions to the locally running Ollama API and keeps answers in browser memory.
It does not persist questions or include analytics. Dependency/model downloads need
internet; this is a local app rather than a publicly hosted inference service.
Privacy statements apply to this source configuration, not every Ollama installation
or browser extension.

## Verification

```powershell
cd backend
uv run python -m unittest -v
```

```powershell
cd frontend
npm run build
```

Backend tests use mocked Ollama transport to verify mode instructions, invalid input,
connection failures, timeouts, unavailable models, empty/truncated answers, and the
Qwen reasoning prefix seen during the first live check. Real generation receipts
are saved in [submission/live-answers.json](submission/live-answers.json) as checks
completed. Browser verification and the final evidence boundary are recorded in
[submission/VERIFICATION.md](submission/VERIFICATION.md).
The Java role update has a separate [real browser example receipt](submission/live-java-example.json).

A [60-second captioned walkthrough](submission/demo/interview-buddy-demo.mp4) uses
real app captures of all four modes. Inference waiting time is omitted; it is a
still-image walkthrough without audio. See `submission/demo/demo-manifest.json`
for scene timing and `render_demo.py` for the render source.

## Limits

- Answers can be wrong. Check technical details against official documentation.
- Local generation can be slow; it depends on your hardware and model loading.
- Complex requests can reach the answer limit. Ask for a focused snippet or concept.
- This is concept practice, not a company question predictor, DSA judge, resume
  service, automated candidate assessment, or guarantee of an offer.
- Friend testing and any public deployment must be established separately.
- Commits after October 5, 2026 at 06:59 UTC must be noted here, in accordance with
  the challenge rules. No post-deadline changes are recorded yet.

## Open-source components

Project code is MIT licensed. Qwen3 4B weights use Apache 2.0; model weights are not
included in this repository. Ollama, FastAPI, Uvicorn, httpx, React, Vite, and
react-markdown are separate upstream projects with their own license notices.
Dependency lockfiles record the installed versions. See the
[Qwen model page](https://ollama.com/library/qwen3:4b) and
[Qwen release](https://qwenlm.github.io/blog/qwen3/) for model provenance.

Codex assisted with research, implementation, tests, and submission preparation.
The supplied Suniye submission inspired the evidence-focused presentation; its
code, family story, screenshots, integrations, and results are not part of this app.
