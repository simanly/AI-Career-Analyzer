CAREERS = {
    "backend-developer": {
        "name": "Backend Developer",
        "required_skills": [
            "Python",
            "Django",
            "FastAPI",
            "SQL",
            "Git"
        ]
    },

    "machine-learning-engineer": {
        "name": "Machine Learning Engineer",
        "required_skills": [
            "Python",
            "Machine Learning",
            "Pandas",
            "scikit-learn",
            "TensorFlow",
            "NumPy"
        ]
    },

    "data-scientist": {
        "name": "Data Scientist",
        "required_skills": [
            "Python",
            "SQL",
            "Pandas",
            "scikit-learn",
            "Machine Learning",
            "NumPy"
        ]
    },

    "frontend-developer": {
        "name": "Frontend Developer",
        "required_skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React"
        ]
    }
}


def predict_careers(skills: list[str]) -> list[dict]:
    results = []

    user_skills = {skill.lower() for skill in skills}

    for career_id, career in CAREERS.items():
        required_skills = career["required_skills"]

        matched_skills = [
            skill
            for skill in required_skills
            if skill.lower() in user_skills
        ]

        score = len(matched_skills) / len(required_skills)

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower() not in user_skills
        ]

        results.append({
            "career_id": career_id,
            "career_name": career["name"],
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    results.sort(
        key=lambda career: career["score"],
        reverse=True
    )

    return results