import re

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

# Tam söz uyğunluğu: "Git" → "digital", "CSS" → "success" kimi yalançı tapıntıların qarşısını alır.
SKILL_PATTERNS = {
    skill: re.compile(r"(?<![a-z0-9])" + re.escape(skill.lower()) + r"(?![a-z0-9])")
    for skill in SKILLS
}


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()

    return [
        skill for skill, pattern in SKILL_PATTERNS.items()
        if pattern.search(text_lower)
    ]
