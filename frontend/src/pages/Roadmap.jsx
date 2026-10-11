import { Link, Navigate } from "react-router-dom";

export default function Roadmap({ result }) {
  if (!result) return <Navigate to="/upload" replace />;

  const steps = [...(result.roadmap || [])].sort((a, b) => a.step - b.step);
  const totalWeeks = steps.reduce((sum, s) => sum + s.duration_weeks, 0);

  return (
    <div className="page">
      <h2>Learning roadmap</h2>
      <p className="muted">
        {steps.length} steps, about {totalWeeks} weeks
      </p>

      {steps.length === 0 && <p>No roadmap available.</p>}

      <div className="timeline">
        {steps.map((s) => (
          <div className="timeline-item" key={s.step}>
            <div className="timeline-dot">{s.step}</div>
            <div className="card timeline-card">
              <div className="timeline-head">
                <h3>{s.skill}</h3>
                <span className={`badge ${s.priority}`}>{s.priority}</span>
              </div>
              <p className="muted">Duration: {s.duration_weeks} weeks</p>
              <ul>
                {(s.resources || []).map((r) => (
                  <li key={r.url}>
                    <a href={r.url} target="_blank" rel="noreferrer">{r.title}</a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>

      <Link to="/results" className="btn secondary">Back to results</Link>
    </div>
  );
}