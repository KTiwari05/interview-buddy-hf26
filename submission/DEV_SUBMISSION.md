---
title: "Interview Buddy: understand the concept, then find your words"
published: false
tags: devchallenge, weekendchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Weekend Challenge: Build for a Friend](https://dev.to/challenges/hacktoberfest-weekend-2026-10-01).*

## What I Built

I built this for my friend Raj, who is preparing for Java backend developer interviews.
The practice target is medium difficulty. I chose a small starting point: refreshing
backend concepts and turning an explanation into words he can rehearse aloud.
This is one part of that preparation, not a complete Java backend interview curriculum.

I built Interview Buddy, a local companion for practising Java backend interview concepts.
It takes one question and explains it four ways: a clear explanation, a simpler
analogy, a small example, and a concise interview answer. The aim is to help someone
move from recognising a concept to explaining it without looking at the screen.

I used public Indian developer discussions to sharpen the design. A
[September 26 post](https://www.reddit.com/r/developersIndia/comments/1wqvi58/backend_ai_in_2026_what_should_i_actually_prepare/)
described uncertainty about dividing time between DSA, backend fundamentals, and AI.
A [September 4 post](https://www.reddit.com/r/developersIndia/comments/1w71odp/as_an_interviewer_what_are_you_expecting_from_a/)
described understanding AI-written code while struggling to write independently.
These are individual accounts, not a survey of hiring practices. They helped me
choose starter questions and keep the workflow focused on understanding.

The interface offers starting points for databases, Spring Boot constructor injection,
design tradeoffs, Java HashMap,
and project decisions. After each answer, it asks the learner to look away and say
the idea in their own words. Switching modes keeps the question fixed, so the
learner can connect the explanation to an example and then to an interview response.

## Demo

[Watch or download the video walkthrough (MP4)](https://raw.githubusercontent.com/KTiwari05/interview-buddy-hf26/main/submission/demo/interview-buddy-demo.mp4).

![Interview Buddy interface with Java and Spring Boot starters](https://raw.githubusercontent.com/KTiwari05/interview-buddy-hf26/main/submission/demo/01-home.jpg)

The 60-second walkthrough uses a database-indexing question in the four modes,
then shows a Java HashMap example. It uses real local Qwen replies. Generation waiting time is edited
out; measured timings are visible in the app and recorded in the evidence notes.

## Code

[Interview Buddy source on GitHub](https://github.com/KTiwari05/interview-buddy-hf26)

The application code is MIT licensed. Qwen3 4B model weights are not bundled with
the project and retain their Apache 2.0 license.

## How I Built It

The frontend uses React and Vite. A FastAPI endpoint selects an instruction for the
requested mode and calls Qwen3 4B through Ollama's local chat API using httpx.
React Markdown renders explanations and code blocks without enabling raw HTML.
The prompts target medium difficulty Java backend practice, and code examples
default to Java or SQL. The application server itself is written in Python.

```text
Question + mode → React → FastAPI → Ollama → Qwen3 4B
```

I kept the implementation small: no account system, database, RAG, agents, or paid
model API. Questions and replies stay in browser memory; the app does not save
conversations. Choosing another mode sends the original question with a different
instruction rather than pretending to maintain a long conversation.

One live check exposed a detail I would have missed with mocks alone. Qwen returned
a reasoning prefix despite thinking being disabled. I added Qwen's `/no_think`
instruction and removed a remaining prefix before displaying the final answer,
then added a regression test. A later check hit the response token limit, so I
shortened the instructions and increased the generation budget. Slow inference is
still a limitation on this computer.

Seven backend tests passed, and the production frontend build completed. I checked
all four modes with real Qwen replies both through the API and in the browser.
I also checked blank input, starter-question resets, and a 375-pixel phone layout
without horizontal overflow. The captured browser replies took approximately
66–223 seconds on this computer. I ran one generated SQL indexing example in
SQLite and confirmed its query plan used the index; that does not validate every
answer the model might generate. The repository's verification notes preserve
the scope of these checks.

After aligning the prompts and starters with Java backend preparation, I reran the
tests and build. A real Java HashMap snippet generated in 82.17 seconds, compiled,
and returned the expected word counts. A broader full-program request hit the
answer limit; the interface displayed the error and recovered on a focused snippet
request. This version works best with one concrete concept or small example at a time.

I have not measured whether the app improves interview outcomes. Friend feedback
is also pending. This version gives a focused practice workflow; its explanations
can still contain errors and should be checked against technical documentation.

## Why Does Open Innovation Matter?

Qwen3 4B does the core work: each explanation is generated by an open-weight model
running through Ollama on this computer. Once dependencies and weights are
downloaded, the inference path uses local endpoints and does not require a paid
model account or send the question to a hosted model provider.

I can inspect and change the prompts, reproduce a bad reply, and change the model
configuration. I tested Qwen3 4B; other models are not yet verified. This gives me
control over the learning workflow, with a clear tradeoff: local hardware limits
response speed and the model's answers still need scrutiny.

The benefit is control over where inference runs and how explanations are requested.
I am not claiming that this small model is more accurate than a closed model.

## My Agent Session

Codex helped review the brief, research public discussions, implement the app,
run checks, and prepare this post. I reviewed the results before publication.

## Prize Categories

I am entering the overall challenge. This implementation uses Qwen and Ollama;
I am not claiming any partner prize category.
