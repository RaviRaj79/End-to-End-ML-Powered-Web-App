import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './styles.css';

const API = import.meta.env.VITE_API_URL || (import.meta.env.DEV ? 'http://localhost:8000' : '');
const demo = {
  candidate_name: 'Alex Johnson',
  job_title: 'Machine Learning Engineer',
  resume_text: 'Python developer with hands-on experience building React dashboards and FastAPI REST APIs. Used Pandas, NumPy, scikit-learn and SQL to ship machine learning projects. Containerized applications with Docker and automated testing with GitHub Actions.',
  job_description: 'We seek a Machine Learning Engineer skilled in Python, scikit-learn, Pandas, NumPy, SQL, Docker, AWS and CI/CD. You will build REST API services and collaborate using Git and Agile practices.'
};

function App() {
  const [form, setForm] = useState(demo), [result, setResult] = useState(null), [history, setHistory] = useState([]), [loading, setLoading] = useState(false), [error, setError] = useState('');
  const loadHistory = () => fetch(`${API}/api/matches`).then(r => r.json()).then(setHistory).catch(() => {});
  useEffect(() => { loadHistory(); }, []);
  const update = e => setForm({ ...form, [e.target.name]: e.target.value });
  const loadResume = async e => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) return setError('Please choose a PDF smaller than 5 MB.');
    setLoading(true); setError('');
    try {
      const body = new FormData(); body.append('file', file);
      const response = await fetch(`${API}/api/resume-text`, { method: 'POST', body });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'The PDF could not be read.');
      setForm(current => ({ ...current, resume_text: data.text }));
    } catch (err) { setError(err.message || 'Could not reach the API. Start the FastAPI backend on port 8000.'); } finally { setLoading(false); }
  };
  const submit = async e => {
    e.preventDefault(); setLoading(true); setError('');
    try {
      const res = await fetch(`${API}/api/matches`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(form) });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.detail || `Analysis failed (${res.status}).`);
      setResult(data); loadHistory();
    } catch (err) { setError(err.message || 'Could not reach the API. Start the FastAPI backend on port 8000.'); } finally { setLoading(false); }
  };
  return <main>
    <nav><span className="logo">✦ TalentMatch <i>AI</i></span><div className="nav-links"><span>How it works</span><span>Privacy first</span><button className="nav-cta" onClick={() => document.querySelector('form').scrollIntoView({behavior:'smooth'})}>Analyze a role</button></div></nav>
    <section className="hero"><div className="hero-copy"><p className="eyebrow">EXPLAINABLE CAREER INTELLIGENCE</p><h1>Make every application count.</h1><p>Turn your experience into a clear, evidence-backed view of role fit—then know exactly what to improve next.</p><div className="hero-proof"><b>91%</b><span>of skills made visible<br/>in one focused report</span><b>∞</b><span>career paths,<br/>one clear signal</span></div></div><HeroVisual /></section>
    <section className="trust"><span>BUILT FOR FOCUSED JOB SEEKERS</span><div><b>Skill coverage</b><b>Semantic relevance</b><b>Actionable feedback</b><b>Private by design</b></div></section>
    <div className="layout">
      <form onSubmit={submit} className="panel form-panel">
        <div className="form-top"><h2>Create a match</h2><button type="button" className="text-btn" onClick={() => setForm(demo)}>Load demo</button></div>
        <label>Candidate name<input name="candidate_name" value={form.candidate_name} onChange={update}/></label>
        <label>Target role<input name="job_title" value={form.job_title} onChange={update}/></label>
        <label>Resume / profile<textarea name="resume_text" value={form.resume_text} onChange={update}/></label>
        <label className="upload"><input type="file" accept=".pdf,application/pdf" onChange={loadResume}/><span>↥</span> Upload your resume PDF <small>up to 5 MB · or paste above</small></label>
        <label>Job description<textarea name="job_description" value={form.job_description} onChange={update}/></label>
        {error && <p className="error">{error}</p>}<button className="primary" disabled={loading}>{loading ? 'Analyzing…' : 'Analyze match →'}</button>
      </form>
      <section className="right-col">
        {result ? <Results result={result} /> : <div className="panel empty"><span>◎</span><h2>Ready when you are</h2><p>Run an analysis to see an explainable match report.</p></div>}
        <div className="panel history"><h2>Recent analyses</h2>{history.length ? history.map(item => <div className="history-row" key={item.id}><div><strong>{item.job_title}</strong><small>{item.candidate_name}</small></div><b>{item.score}%</b></div>) : <p className="muted">Your saved analyses will appear here.</p>}</div>
      </section>
    </div>
  </main>;
}
function Chips({items, kind}) { return <div className="chips">{items.length ? items.map(x => <span className={kind} key={x}>{x}</span>) : <span className="muted">None detected</span>}</div> }
function Results({result}) { return <div className="panel results"><div className="score-row"><div className="score"><b>{result.score}</b><span>% match</span></div><div><p className="eyebrow">MATCH ASSESSMENT</p><h2>{result.fit_level}</h2><p className="muted">A combined semantic and skills-based score.</p></div></div><div className="result-grid"><article><h3>✓ Matched skills</h3><Chips items={result.matched_skills} kind="good" /></article><article><h3>＋ Growth areas</h3><Chips items={result.missing_skills} kind="warn" /></article></div><article className="advice"><h3>Next best moves</h3><ul>{result.recommendations.map(r => <li key={r}>{r}</li>)}</ul></article></div> }
function HeroVisual() { return <div className="visual" aria-label="Abstract AI matching illustration"><div className="visual-grid"></div><div className="orbit orbit-one"></div><div className="orbit orbit-two"></div><div className="node node-a">PY</div><div className="node node-b">SQL</div><div className="node node-c">ML</div><div className="match-core"><span>ROLE<br/>FIT</span><b>87%</b></div><div className="resume-card"><div className="card-mark">✦</div><strong>Candidate profile</strong><i></i><i></i><i className="short"></i><div><span></span><span></span><span></span></div></div><div className="signal-card"><span className="pulse"></span><b>High alignment</b><small>Skill signal detected</small></div></div> }
createRoot(document.getElementById('root')).render(<App />);
