# Step 4: CV text -> top matching vacancies (TF-IDF + cosine similarity).
import pandas as pd, sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("vacancies_clean.csv")
df["doc"] = (df["job_title"] + " ") * 3 + df["skills"].fillna("") + " " + df["description"]

vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=50000)
X = vec.fit_transform(df["doc"])

def match(cv_text, top=5):
    sims = cosine_similarity(vec.transform([cv_text]), X)[0]
    out = df.assign(score=(sims * 100).round(1)).nlargest(top, "score")
    return out[["job_title", "job_group", "score", "Link"]]

def gap(cv_text, row_skills):
    need = {s.strip() for s in str(row_skills).split(",") if s.strip()}
    have = {s for s in need if s in cv_text.lower()}
    return sorted(need - have)          # missing skills

if __name__ == "__main__":
    cv = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else \
         "Python SQL pandas data analysis excel power bi ingilis dili"
    print(match(cv))