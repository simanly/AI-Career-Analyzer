import pandas as pd
import numpy as np

np.random.seed(42)

careers = [
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "Cloud Engineer",
    "QA Automation Engineer"
]

skills = [
    "python",
    "sql",
    "machine_learning",
    "statistics",
    "pandas",
    "numpy",
    "scikit_learn",
    "pytorch",
    "docker",
    "javascript"
]

rows = []

for i in range(120):
    row = {
        "profile_id": f"P{i+1:04d}",
        "years_experience": np.random.randint(0, 6),
        "projects_count": np.random.randint(0, 8),
        "certifications_count": np.random.randint(0, 5),
    }

    for skill in skills:
        row[f"skill_{skill}"] = np.random.randint(0, 4)

    row["career_class"] = np.random.choice(careers)

    rows.append(row)

df = pd.DataFrame(rows)

df.to_csv("data/raw/profiles_test.csv", index=False)

print("Dataset created!")
print(df.head())
print(df.shape)