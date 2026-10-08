def calculate_skill_gap(careers: list[dict]) -> list[dict]:
    results = []

    for career in careers:
        missing_skills = career["missing_skills"]

        gap_count = len(missing_skills)

        if gap_count == 0:
            priority = "low"
        elif gap_count <= 2:
            priority = "medium"
        else:
            priority = "high"

        results.append({
            "career_id": career["career_id"],
            "career_name": career["career_name"],
            "missing_skills": missing_skills,
            "gap_count": gap_count,
            "priority": priority
        })

    return results