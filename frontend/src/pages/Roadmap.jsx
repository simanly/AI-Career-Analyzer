import { Link, Navigate } from "react-router-dom";

const label = (k) => {
  const s = k.replace(/_/g, " ");
  return s.charAt(0).toUpperCase() + s.slice(1);
};

function Detail({ name, value }) {
  if (Array.isArray(value)) {
    if (value.length === 0) return null;
    return (
      <div>
        <p className="muted">{label(name)}</p>
        <ul>
          {value.map((item, i) => {
            if (typeof item === "string") return <li key={i}>{item}</li>;
            const text = item?.title ?? item?.name ?? item?.resource ?? JSON.stringify(item);
            return (
              <li key={i}>
                {item?.url ? (
                  <a href={item.url} target="_blank" rel="noreferrer">{text}</a>
                ) : (
                  text
                )}
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
  if (typeof value === "string" || typeof value === "number") {
    return <p className="muted">{label(name)}: {value}</p>;
  }
  return null;
}

export default function Roadmap({ result }) {
  if (!result) return <Navigate to="/upload" replace />;

  const score = Object.fromEntries(result.careers.map((c) => [c.id, c.score]));
  const items = [...result.roadmap].sort(
    (a, b) => (score[b.id] ?? 0) - (score[a.id] ?? 0)
  );

  return (
    <div className="page">
      <h2>Learning roadmap</h2>
      <p className="muted">Steps for each career, best match first.</p>

      {items.length === 0 && <p>No roadmap available.</p>}

      {items.map((r, i) => (
        <details className="road-career" key={r.id ?? i} open={i === 0}>
          <summary>
            <strong>{r.career}</strong>
            <span className="muted"> · {Math.round((score[r.id] ?? 0) * 100)}% match</span>
          </summary>

          {r.steps.length === 0 && (
            <p className="muted">No roadmap steps available for this career yet.</p>
          )}

          <div className="timeline">
            {r.steps.map((step, j) => {
              const isText = typeof step === "string";
              const title = isText ? step : step.skill ?? step.title ?? `Step ${j + 1}`;
              const rest = isText
                ? []
                : Object.entries(step).filter(([k]) => k !== "skill" && k !== "title");
              return (
                <div className="timeline-item" key={j}>
                  <div className="timeline-dot">{j + 1}</div>
                  <div className="card timeline-card">
                    <h3>{title}</h3>
                    {rest.map(([k, v]) => (
                      <Detail key={k} name={k} value={v} />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </details>
      ))}

      <Link to="/results" className="btn secondary">Back to results</Link>
    </div>
  );
}