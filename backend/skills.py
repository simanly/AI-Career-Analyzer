SKILLS = [
    "Python",
    "SQL",
    "Django",
    "FastAPI",
    "React",
    "JavaScript",
    "HTML",
    "CSS",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "scikit-learn",
    "Machine Learning",
    "NLP",
    "Docker",
    "Git",
    "GitHub",
    "Modbus TCP",
    "pytest",
    "Web Scraping",
]


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills