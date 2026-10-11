import { Link } from "react-router-dom";

const STEPS = [
  { n: "01", title: "Analyze", text: "Analyzes your CV and skills" },
  { n: "02", title: "Predict", text: "Predicts suitable career paths" },
  { n: "03", title: "Skill gaps", text: "Identifies your skill gaps" },
  { n: "04", title: "Roadmap", text: "Creates a personalized learning roadmap" },
];

const FEATURES = [
  "Upload your CV and get automatic analysis",
  "Extract skills using advanced NLP",
  "Predict career paths with machine learning",
  "Identify skill gaps and get personalized advice",
  "Generate tailored learning roadmaps",
  "Get career match scores and smart recommendations",
];

export default function Home() {
  return (
    <div className="page">
      <section className="hero">
        <h1>AI Career &amp; Skill Analyzer</h1>
        <p>Upload your CV to discover suitable careers and the skills you are missing.</p>
        <Link to="/upload" className="btn">Get Started</Link>
      </section>

      <section>
        <h2>How it works</h2>
        <div className="steps">
          {STEPS.map((s) => (
            <div className="card" key={s.n}>
              <span className="step-n">{s.n}</span>
              <h3>{s.title}</h3>
              <p>{s.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Key features</h2>
        <ul className="feature-list">
          {FEATURES.map((f) => (
            <li key={f}>{f}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}