import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import Markdown from 'react-markdown';
import './style.css';

const modes = [
  { id: 'explain', label: 'Explain', hint: 'Understand the concept', icon: '≡' },
  { id: 'simpler', label: 'Explain simpler', hint: 'Start with an analogy', icon: '↘' },
  { id: 'example', label: 'Show example', hint: 'Connect it to real code', icon: '</>' },
  { id: 'interview', label: 'Interview answer', hint: 'Practise saying it aloud', icon: '“' },
];
const starters = [
  { topic: 'Databases', label: 'Why use an index?', question: 'What is database indexing, and when can adding an index be a bad idea?' },
  { topic: 'Spring', label: 'Why constructor injection?', question: 'Why use constructor injection in Spring Boot, and how does it make unit testing easier?' },
  { topic: 'Design', label: 'SQL or NoSQL?', question: 'Why would I choose PostgreSQL over a document database for an order management system? Explain the tradeoffs.' },
  { topic: 'Java', label: 'Explain HashMap', question: 'How does HashMap work in Java, and what happens when two keys have the same hash?' },
  { topic: 'Projects', label: 'Explain a design choice', question: 'How should I explain a technical design decision from my project in an interview? Give a structure without inventing my experience.' },
];

function App() {
  const [question, setQuestion] = useState('');
  const [mode, setMode] = useState('explain');
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [connection, setConnection] = useState('checking');

  useEffect(() => {
    fetch('/api/health').then(response => setConnection(response.ok ? 'ready' : 'offline'))
      .catch(() => setConnection('offline'));
  }, []);

  async function ask(nextMode = mode) {
    if (!question.trim() || busy) return;
    setMode(nextMode);
    setBusy(true);
    setError('');
    try {
      const response = await fetch('/api/ask', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: question.trim(), mode: nextMode }),
      });
      const data = await response.json();
      if (!response.ok) {
        setError(typeof data.detail === 'string' ? data.detail : 'Check your question and try again.');
        if (response.status === 503) setConnection('offline');
        return;
      }
      setResult({ ...data, question: question.trim(), mode: nextMode });
      setConnection('ready');
    } catch {
      setError('Could not reach the app. Check that the backend is running, then try again.');
      setConnection('offline');
    } finally {
      setBusy(false);
    }
  }

  function chooseStarter(starter) {
    setQuestion(starter.question);
    setMode('explain');
    setResult(null);
    setError('');
  }

  return (
    <div className="app-shell">
      <header className="masthead">
        <a className="brand" href="/" aria-label="Interview Buddy home"><span className="brand-mark">ib<span>•</span></span><span>interview buddy</span></a>
        <span className={`connection ${connection}`} role="status"><i />{connection === 'ready' ? 'Local AI ready' : connection === 'checking' ? 'Checking local AI' : 'Local AI unavailable'}</span>
      </header>

      <main>
        <section className="intro" aria-labelledby="page-title">
          <p className="eyebrow">YOUR NEXT INTERVIEW STARTS WITH UNDERSTANDING</p>
          <h1 id="page-title">Know the concept.<br /><span>Find your words.</span></h1>
          <p className="intro-copy">One question, four ways to get it. Turn Java backend concepts into explanations you can actually say out loud.</p>
        </section>

        <div className="workspace">
          <section className="question-panel" aria-labelledby="question-title">
            <div className="panel-heading"><h2 id="question-title">What are you working on?</h2><span className="small-label">YOUR QUESTION</span></div>
            <form onSubmit={event => { event.preventDefault(); ask(); }}>
              <label htmlFor="question">A concept, a code snippet, or a project decision</label>
              <textarea id="question" value={question} onChange={event => setQuestion(event.target.value)} disabled={busy} maxLength={4000} placeholder="For example: Why does an index make a query faster, and what does it cost?" rows={6} />
              <div className="question-footnote"><span>Start with one thing you want to understand.</span><span>{question.length}/4000</span></div>
              <fieldset disabled={busy} className="mode-options">
                <legend>How would you like to practise?</legend>
                {modes.map(item => <button key={item.id} type="button" aria-pressed={mode === item.id} className={`mode-button ${mode === item.id ? 'selected' : ''}`} onClick={() => result && result.question === question.trim() ? ask(item.id) : setMode(item.id)}><span className="mode-icon" aria-hidden="true">{item.icon}</span><span><strong>{item.label}</strong><small>{item.hint}</small></span><span className="mode-dot" aria-hidden="true" /></button>)}
              </fieldset>
              <button className="ask-button" type="submit" disabled={busy || !question.trim()}>{busy ? 'Preparing your answer…' : 'Let’s work through it'}<span aria-hidden="true">↗</span></button>
              {error && <p className="error" role="alert">{error}</p>}
            </form>
            <div className="starter-section"><p className="small-label">NEED A STARTING POINT?</p><div className="starters">{starters.map(starter => <button key={starter.topic} disabled={busy} onClick={() => chooseStarter(starter)}><small>{starter.topic}</small><span>{starter.label}<b aria-hidden="true">↗</b></span></button>)}</div></div>
          </section>

          <section className="answer-panel" aria-labelledby="answer-title" aria-busy={busy}>
            <div className="answer-heading"><div><p className="small-label">YOUR PRACTICE SHEET</p><h2 id="answer-title">{result ? modes.find(item => item.id === result.mode).label : 'Make it click.'}</h2></div><span className="sheet-corner" aria-hidden="true">✳</span></div>
            {busy ? <div className="waiting" role="status"><div className="waiting-line" /><h3>Working through your question</h3><p>Your local model is preparing an answer. The first response may take longer while it loads.</p></div> : result ? <div className="answer-content"><p className="answered-question">{result.question}</p><article className="markdown"><Markdown>{result.answer}</Markdown></article><div className="answer-receipt"><span>{result.model} · on this computer</span><span>{result.seconds}s</span></div><div className="practice-note"><strong>Now make it yours.</strong><p>Look away from the answer. Explain the idea in your own words, then try another mode.</p></div></div> : <div className="empty-answer"><div className="concept-diagram" aria-hidden="true"><span>?</span><i /><span className="idea">!</span><i /><span className="speech">“ ”</span></div><h3>From “I’ve seen this”<br />to “I can explain this.”</h3><p>Ask a question on the left. Your answer will appear here, with a different perspective whenever you need one.</p><div className="empty-steps"><span>Understand</span><span>See it in action</span><span>Say it aloud</span></div></div>}
            <p className="answer-disclaimer">AI can make mistakes. Check technical claims against documentation.</p>
          </section>
        </div>
      </main>
      <footer><span>Built for the moments when a concept won’t click.</span><span>Local inference · No account · No saved conversations</span></footer>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
