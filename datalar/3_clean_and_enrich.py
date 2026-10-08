# Step 3: merge, clean, and add new columns (skills, seniority, job group).
import pandas as pd, re

a = pd.read_csv("hellojob_150_sehife.csv")
b = pd.read_csv("hellojob_details.csv")
df = a.merge(b, on="Link", how="left")

# clean title: remove the "PREMİUM" line
df["job_title"] = df["Vakansiya adı"].str.split("\n").str[0].str.strip()
df["is_premium"] = df["Vakansiya adı"].str.contains("PREMİUM", na=False)
df = df.drop_duplicates("Link").dropna(subset=["description"])
df["description"] = df["description"].str.replace(r"\s+", " ", regex=True)

# skills dictionary (add your own)
SKILLS = ["python", "sql", "excel", "power bi", "java", "javascript", "react", "docker",
          "photoshop", "figma", "1c", "sap", "seo", "smm", "crm", "autocad",
          "ingilis dili", "rus dili", "ms office", "word", "satış", "mühasibat",
          "marketinq", "komunikasiya", "sürücülük"]
def find_skills(t):
    t = str(t).lower()
    return ", ".join(s for s in SKILLS if s in t)
df["skills"] = (df["job_title"] + " " + df["description"]).apply(find_skills)

# experience in years (number from text like "1-3 il")
df["exp_years"] = df["experience"].astype(str).str.extract(r"(\d+)").astype(float)
df["seniority"] = pd.cut(df["exp_years"], [-1, 0, 2, 5, 50], labels=["entry", "junior", "middle", "senior"])

# job group from title keywords (simple rules)
GROUPS = {
    "IT": ["developer", "proqramçı", "it ", "data", "qa", "devops"],
    "Satış": ["satış", "satıcı", "menecer"],
    "Maliyyə": ["mühasib", "maliyyə", "audit"],
    "Marketinq": ["marketinq", "smm", "dizayner", "kontent"],
    "Xidmət": ["operator", "kuryer", "xadimə", "təhlükəsizlik", "ofisiant"],
}
def group(t):
    t = t.lower()
    for g, kws in GROUPS.items():
        if any(k in t for k in kws):
            return g
    return "Digər"
df["job_group"] = df["job_title"].apply(group)

df.to_csv("vacancies_clean.csv", index=False, encoding="utf-8-sig")
print(df.shape); print(df.isna().mean().round(2))