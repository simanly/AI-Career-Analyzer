import { Link, Navigate } from "react-router-dom";

const PRIORITY_LABEL = { high: "High", medium: "Medium", low: "Low" };

export default function Results({ result }) {
  if (!result) return <Navigate to="/upload" replace />;

  const careers = [...result.careers].sort((a, b) => b.score - a.score);

  return (
    <div className="page">
      <h2>Nəticələr</h2>

      <section>
        <h3>Tapılan bacarıqlar</h3>
        <div className="chips">
          {result.skills.map((s) => (
            <span className="chip" key={s}>{s}</span>
          ))}
        </div>
      </section>

      <section>
        <h3>Uyğun karyeralar</h3>
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

      <Link to="/upload" className="btn secondary">Yeni CV yüklə</Link>
    </div>
  );
}