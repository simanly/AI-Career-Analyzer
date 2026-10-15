from pathlib import Path
import joblib

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


def predict_resume_category(resume_text: str) -> dict:
    if model is None:
        raise RuntimeError(
            "ML modeli tapılmadı. Əvvəl train_model.py faylını işə sal."
        )

    if not isinstance(resume_text, str) or not resume_text.strip():
        raise ValueError("CV mətni boş ola bilməz.")

    prediction = model.predict([resume_text])[0]

    probabilities = None
    if hasattr(model, "predict_proba"):
        class_probabilities = model.predict_proba([resume_text])[0]
        probabilities = {
            str(label): round(float(probability), 4)
            for label, probability in zip(
                model.classes_, class_probabilities
            )
        }

    return {
        "predicted_category": str(prediction),
        "probabilities": probabilities
    }