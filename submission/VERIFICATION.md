# Verification receipts — October 4, 2026

## Application checks

- Final production frontend build passed: Vite 7.3.6, 191 modules transformed.
- Seven backend unittest cases passed: all four mode instructions and input trimming,
  validation before inference, unavailable Ollama, timeout, empty/truncated replies,
  model availability, and Qwen reasoning-prefix removal. External failures are mocked.
- Four real `/ask` calls to local Qwen3 4B succeeded. The complete replies and measured
  timings are in `live-answers.json`: 104.83, 61.94, 57.46, and 84.44 seconds.
- All four modes also completed in the browser against the real backend. Captures are
  in `demo/`. Explain: 66.13 s; simpler: 70.36 s; example: about 66 s;
  interview: 223.08 s. Timings describe this computer, not a benchmark.
- Blank/whitespace input disables submission. An earlier API-starter check reset
  the answer and selected Explain with the original FastAPI question. The final
  Java-role check confirmed the replacement Spring Boot starter question.
- At a 375 by 812 viewport, document scroll width was 360 px: no horizontal page overflow.
  The completed interview answer was captured at that width. The temporary override
  was then reset. No browser warnings/errors were reported by the captured console.
- The SQL example from the direct live example reply ran with Python's SQLite:
  `CREATE INDEX idx_name ON users(name)` and a lookup for Alice. It returned the
  expected row and the query plan used the index. This does not verify every model answer.

## Java role update

The final prompts target medium difficulty Java backend practice and Java/SQL code
examples. Spring Boot constructor injection and Java HashMap replace the earlier
FastAPI/DSA starter wording. The seven backend tests and production build passed
again after this change. The browser showed the new Spring starter question.
A real Java example completed in 82.17 seconds; the rendered snippet was wrapped
with imports and a main method, compiled with javac 20.0.1, and executed with checks
for `java = 2` and `spring = 1`. See `live-java-example.json` for the rendered code.
A preceding request for a complete Java program reached the response token limit;
the app displayed its specific error and successfully recovered on a narrower request.
The four SQL/indexing captures predate this prompt update; they demonstrate the
same four-mode interface. The final video adds the actual Java example capture.

The final 60-second MP4 is H.264, yuv420p, 1600 by 1000, 24 fps, without audio.
FFmpeg decoded all 1,440 frames successfully. All seven scenes were visually
checked in a contact sheet. These are structural and still-frame checks, not an
audio-listening test or independent playback checks on every device.

## Boundaries

No measured interview outcomes or friend feedback. The user identified Raj as a
real friend preparing for Java backend developer interviews and specified medium
difficulty. No detailed interview failure, employer, seniority history, or feedback
has been invented. No deployed hosted model service,
production load test, or verification of other operating systems/models. Local model
latency can exceed three minutes. The app is a learning aid; generated explanations
can be wrong. Browser captures are real; the video omits inference waiting time and
is a captioned still-image walkthrough, without narration or simulated mouse actions.

Public repository contents and a public demo URL must be checked after publication.
The DEV article remains a draft until its real-person requirement and public links
are complete. A local ZIP, local video, or localhost URL is not a submitted entry.
