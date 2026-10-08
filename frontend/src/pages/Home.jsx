import { Link } from "react-router-dom";

const STEPS = [
  { n: "01", title: "Analyze", text: "CV və bacarıqlarını analiz edir" },
  { n: "02", title: "Predict", text: "Uyğun karyera yollarını tapır" },
  { n: "03", title: "Skill gaps", text: "Çatışmayan bacarıqları göstərir" },
  { n: "04", title: "Roadmap", text: "Fərdi öyrənmə planı hazırlayır" },
];

export default function Home() {
  return (
    <div className="page">
      <section className="hero">
        <h1>AI Career &amp; Skill Analyzer</h1>
        <p>CV-ni yüklə, uyğun karyeranı və çatışmayan bacarıqları gör.</p>
        <Link to="/upload" className="btn">Get Started</Link>
      </section>

      <section className="steps">
        {STEPS.map((s) => (
          <div className="card" key={s.n}>
            <span className="step-n">{s.n}</span>
            <h3>{s.title}</h3>
            <p>{s.text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}