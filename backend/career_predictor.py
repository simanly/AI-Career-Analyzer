from pathlib import Path
import joblib

import resume_features  # noqa: F401  (model pickle-ı bu modula istinad edir)

CAREERS = {
    "backend-developer": {
        "name": "Backend Developer",
        "required_skills": [
            "Python", "Django", "FastAPI", "SQL", "Git"
        ]
    },
    "machine-learning-engineer": {
        "name": "Machine Learning Engineer",
        "required_skills": [
            "Python", "Machine Learning", "Pandas",
            "scikit-learn", "TensorFlow", "NumPy"
        ]
    },
    "data-scientist": {
        "name": "Data Scientist",
        "required_skills": [
            "Python", "SQL", "Pandas",
            "scikit-learn", "Machine Learning", "NumPy"
        ]
    },
    "data-analyst": {
        "name": "Data Analyst",
        "required_skills": [
            "SQL", "Excel", "Power BI", "Tableau",
            "Python", "Data Visualization"
        ]
    },
    "devops-engineer": {
        "name": "DevOps Engineer",
        "required_skills": [
            "Docker", "Kubernetes", "AWS", "Linux", "Git", "Terraform"
        ]
    },
    "frontend-developer": {
        "name": "Frontend Developer",
        "required_skills": [
            "HTML", "CSS", "JavaScript", "React"
        ]
    }
}

MODEL_PATH = Path(__file__).resolve().parent / "career_text_model.joblib"
model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


def predict_careers(skills: list[str]) -> list[dict]:
    user_skills = {
        skill.strip().lower()
        for skill in skills
        if isinstance(skill, str) and skill.strip()
    }

    results = []

    for career_id, career in CAREERS.items():
        required_skills = career["required_skills"]

        matched_skills = [
            skill for skill in required_skills
            if skill.lower() in user_skills
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill.lower() not in user_skills
        ]

        score = (
            len(matched_skills) / len(required_skills)
            if required_skills else 0
        )

        results.append({
            "career_id": career_id,
            "career_name": career["name"],
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    results.sort(key=lambda career: career["score"], reverse=True)
    return results


def predict_resume_category(resume_text: str, top_k: int = 3) -> dict:
    if model is None:
        raise RuntimeError(
            "ML modeli tapılmadı. Əvvəl train_model.py faylını işə sal."
        )

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("CV mətni boş ola bilməz.")

    class_probabilities = model.predict_proba([resume_text])[0]

    ranked = sorted(
        zip(model.classes_, class_probabilities),
        key=lambda pair: pair[1],
        reverse=True,
    )

    top_predictions = [
        {"category": str(label), "probability": round(float(probability), 4)}
        for label, probability in ranked[:top_k]
    ]

    return {
        "predicted_category": top_predictions[0]["category"],
        "confidence": top_predictions[0]["probability"],
        "top_predictions": top_predictions,
        "probabilities": {
            str(label): round(float(probability), 4)
            for label, probability in ranked
        },
    }
