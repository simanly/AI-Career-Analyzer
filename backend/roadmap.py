ROADMAPS = {
    "NumPy": [
        "Learn NumPy arrays and basic operations",
        "Practice indexing, slicing and reshaping",
        "Practice matrix operations",
        "Build a small data analysis project"
    ],

    "HTML": [
        "Learn HTML structure and semantic tags",
        "Practice forms and tables",
        "Build a simple webpage"
    ],

    "CSS": [
        "Learn CSS selectors and box model",
        "Practice Flexbox and Grid",
        "Build a responsive webpage"
    ],

    "JavaScript": [
        "Learn JavaScript fundamentals",
        "Practice DOM manipulation",
        "Build a small interactive web project"
    ]
}


def default_steps(skill: str) -> list[str]:
    return [
        f"Learn {skill} fundamentals",
        f"Practice {skill} with small exercises",
        f"Build a small project that uses {skill}",
    ]


def generate_roadmap(skill_gap: list[dict]) -> list[dict]:
    roadmap = []

    for career in skill_gap:
        steps = []

        for skill in career["missing_skills"]:
            steps.append({
                "skill": skill,
                "steps": ROADMAPS.get(skill) or default_steps(skill)
            })

        roadmap.append({
            "career_id": career["career_id"],
            "career_name": career["career_name"],
            "steps": steps
        })

    return roadmap