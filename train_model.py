from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "resumes_real.csv"
MODEL_PATH = ROOT / "backend" / "career_text_model.joblib"

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset tapılmadı: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required = {"category", "text"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV-də bu sütunlar olmalıdır: {required}")

    # CV mətnini bacarıq, təhsil və təcrübə məlumatları ilə birləşdiririk.
    text_columns = [c for c in ["text", "skills", "education", "experience"] if c in df.columns]
    df["model_text"] = (
        df[text_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.strip()
    )
    df = df[(df["model_text"] != "") & df["category"].notna()].copy()
    df["category"] = df["category"].astype(str).str.strip()
    df = df[df["category"] != ""]

    X = df["model_text"]
    y = df["category"]

    print("Dataset ölçüsü:", df.shape)
    print("Sinif sayı:", y.nunique())
    print("Sinif bölgüsü:")
    print(y.value_counts().to_string())

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            max_features=40000,
            ngram_range=(1, 2),
            min_df=2,
            sublinear_tf=True
        )),
        ("classifier", LogisticRegression(
            max_iter=1500,
            class_weight="balanced"
        ))
    ])

    print("\nModel öyrədilir...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print("\nTest accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel yadda saxlanıldı: {MODEL_PATH}")

    sample = " ".join(X_test.iloc[:1].tolist())
    print("\nNümunə proqnoz:", model.predict([sample])[0])
    print("Model hazırdır.")

if __name__ == "__main__":
    main()
