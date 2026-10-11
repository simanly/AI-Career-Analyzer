import { Link, Navigate } from "react-router-dom";

const PRIORITY_LABEL = { high: "High", medium: "Medium", low: "Low" };

export default function Results({ result }) {
  if (!result) return <Navigate to="/upload" replace />;

  const careers = [...result.careers].sort((a, b) => b.score - a.score);

  return (
    <div className="page">
      <h2>Results</h2>

      {careers[0] && (
        <section className="top-match">
          <span className="muted">Best career match</span>
          <h3>{careers[0].name}</h3>
          <strong>{Math.round(careers[0].score * 100)}% match</strong>
        </section>
      )}

      <section>
        <h3>Detected skills</h3>
        <div className="chips">
          {result.skills.map((s) => (
            <span className="chip" key={s}>{s}</span>
          ))}
        </div>
      </section>

      <section>
        <h3>Career matches</h3>
        {careers.map((c) => {
          const percent = Math.round(c.score * 100);
          return (
            <div className="career" key={c.id}>
              <div className="career-head">
                <span>{c.name}</span>
                <strong>{percent}%</strong>
              </div>
              <div className="bar">
                <div className="bar-fill" style={{ width: `${percent}%` }} />
              </div>
            </div>
          );
        })}
      </section>

      <section>
        <h3>Skill gap</h3>
        <ul className="gap-list">
          {result.skill_gap.map((g) => (
            <li key={g.skill}>
              <span>{g.skill}</span>
              <span className={`badge ${g.priority}`}>{PRIORITY_LABEL[g.priority]}</span>
            </li>
          ))}
        </ul>
      </section>

      <div className="actions">
        <Link to="/roadmap" className="btn">View learning roadmap</Link>
        <Link to="/upload" className="btn secondary">Upload a new CV</Link>
      </div>
    </div>
  );
}