import random
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics import accuracy_score, classification_report, f1_score, log_loss
from sklearn.model_selection import StratifiedKFold, cross_val_predict, train_test_split
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))

# Model pickle-ında funksiyalar "resume_features" adı ilə saxlanılır;
# backend də eyni modulu import etdiyi üçün yükləmə problemsiz işləyir.
from resume_features import ScaledLinearSVC, body_texts, title_texts  # noqa: E402

DATA_PATH = ROOT / "data" / "raw" / "resumes_real.csv"
SYNTHETIC_PATH = ROOT / "data" / "raw" / "tech_resumes_synthetic.csv"
MODEL_PATH = ROOT / "backend" / "career_text_model.joblib"

TITLE_WEIGHT = 0.5


FIRST_NAMES = ["Farah", "John", "Aysel", "Nijat", "Emily", "Rashad", "Sara", "Michael", "Leyla", "David", "Anna",
               "Elvin", "Maria", "Kamran", "Jessica", "Tural", "Olivia", "Samir", "Laura", "Orkhan", "Daniel",
               "Nigar", "Sophie", "Murad", "Amanda", "Rafael", "Aynur", "James", "Fidan", "Robert"]
LAST_NAMES = ["Martin", "Smith", "Aliyev", "Hatamli", "Johnson", "Mammadov", "Brown", "Huseynova", "Taylor",
              "Guliyev", "Wilson", "Ismayilov", "Clark", "Abbasov", "Lewis", "Rzayeva", "Walker", "Hasanov",
              "Young", "Karimova", "King", "Mustafayev", "Lopez", "Sadigov", "Garcia"]


def add_name_header(texts, seed=0, probability=0.6):
    """Real CV-lərin çoxu ad + soyad ilə başlayır, dataset isə birbaşa vəzifə adı ilə.

    Modelin yalnız ilk sətrə güvənməməsi üçün CV-lərin bir hissəsinə ad əlavə edilir.
    """
    rng = random.Random(seed)
    out = []
    for text in texts:
        if rng.random() < probability:
            name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
            if rng.random() < 0.5:
                name = name.upper()
            text = f"{name} {text}"
        out.append(text)
    return out


def tfidf(**kwargs):
    return TfidfVectorizer(strip_accents="unicode", sublinear_tf=True, **kwargs)


def build_model(temperature: float = 5.0):
    """CV mətni (body) + CV başlığı (title) ayrı vektorlaşdırılır.

    Başlıq vəzifə adını ehtiva etdiyi üçün kateqoriyanın ən güclü siqnalıdır,
    lakin çəkisi azaldılır ki, model yalnız başlığa güvənməsin.
    """
    features = FeatureUnion(
        [
            ("body", Pipeline([
                ("select", FunctionTransformer(body_texts)),
                ("tfidf", tfidf(ngram_range=(1, 1), min_df=2, max_features=150000)),
            ])),
            ("title", Pipeline([
                ("select", FunctionTransformer(title_texts)),
                ("tfidf", tfidf(ngram_range=(1, 2), min_df=1)),
            ])),
        ],
        transformer_weights={"body": 1.0, "title": TITLE_WEIGHT},
    )

    classifier = ScaledLinearSVC(C=1.0, class_weight="balanced")
    classifier.temperature = temperature

    return Pipeline([("features", features), ("classifier", classifier)])


def choose_temperature(decisions, y_true, classes):
    """Out-of-fold SVC xalları üçün log-loss-u minimallaşdıran temperature seçir."""
    best_t, best_loss = None, float("inf")
    for temperature in [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20]:
        scores = decisions * temperature
        scores -= scores.max(axis=1, keepdims=True)
        proba = np.exp(scores)
        proba /= proba.sum(axis=1, keepdims=True)
        loss = log_loss(y_true, proba, labels=classes)
        if loss < best_loss:
            best_t, best_loss = temperature, loss
    return best_t, best_loss


def clean_frame(df, source):
    # API-yə yalnız CV mətni gəlir, ona görə də model də yalnız "text" üzərində öyrədilir.
    df = df.dropna(subset=["text", "category"]).copy()
    df["text"] = df["text"].astype(str)
    df["category"] = df["category"].astype(str).str.strip()
    df = df[(df["text"].str.strip() != "") & (df["category"] != "")]
    df["source"] = source
    return df[["text", "category", "source"]]


def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset tapılmadı: {DATA_PATH}")

    real = pd.read_csv(DATA_PATH)

    required = {"category", "text"}
    if not required.issubset(real.columns):
        raise ValueError(f"CSV-də bu sütunlar olmalıdır: {required}")

    frames = [clean_frame(real, "real")]

    # Real datasetdə proqramçı/data/ML CV-ləri yoxdur; bunlar üçün sintetik data əlavə olunur.
    if SYNTHETIC_PATH.exists():
        frames.append(clean_frame(pd.read_csv(SYNTHETIC_PATH), "synthetic"))
    else:
        print("XƏBƏRDARLIQ: sintetik texniki CV datası tapılmadı (src/create_tech_resumes.py işə sal).")

    df = pd.concat(frames, ignore_index=True)
    df["text"] = add_name_header(df["text"].tolist())
    return df


def main():
    df = load_data()
    X, y = df["text"], df["category"]
    is_real = (df["source"] == "real").to_numpy()

    print("Dataset ölçüsü:", df.shape, df["source"].value_counts().to_dict())
    print("Sinif sayı:", y.nunique())
    print(y.value_counts().to_string())

    # 1) Dürüst qiymətləndirmə: 5-fold cross-validation (yalnız REAL CV-lər üzərində hesablanır)
    cv_decisions = cross_val_predict(
        build_model(), X, y, method="decision_function",
        cv=StratifiedKFold(5, shuffle=True, random_state=0), n_jobs=-1,
    )
    classes = np.array(sorted(y.unique()))
    cv_pred = classes[cv_decisions.argmax(axis=1)]
    temperature, loss = choose_temperature(cv_decisions[is_real], y[is_real], classes)
    print(f"Seçilən temperature: {temperature} (log-loss {loss:.3f})")
    print("\n5-fold CV accuracy (real CV-lər):", round(accuracy_score(y[is_real], cv_pred[is_real]), 4))
    print("5-fold CV macro F1 (real CV-lər):", round(f1_score(y[is_real], cv_pred[is_real], average="macro"), 4))
    print("5-fold CV accuracy (sintetik, optimist!):", round(accuracy_score(y[~is_real], cv_pred[~is_real]), 4))

    # 2) Ayrıca test hissəsi (yalnız hesabat üçün)
    X_train, X_test, y_train, y_test, real_train, real_test = train_test_split(
        X, y, is_real, test_size=0.2, random_state=42, stratify=y
    )
    model = build_model(temperature)
    model.fit(X_train, y_train)

    X_test_real, y_test_real = X_test[real_test], y_test[real_test]
    predictions = model.predict(X_test_real)
    print("\nHold-out test accuracy (real):", round(accuracy_score(y_test_real, predictions), 4))

    probabilities = model.predict_proba(X_test_real)
    top3 = [
        label in model.classes_[row.argsort()[::-1][:3]]
        for label, row in zip(y_test_real, probabilities)
    ]
    print("Hold-out top-3 accuracy (real):", round(sum(top3) / len(top3), 4))
    print("\nClassification report (real):")
    print(classification_report(y_test_real, predictions, zero_division=0))

    # 3) Yekun model bütün data üzərində öyrədilir
    final_model = build_model(temperature)
    final_model.fit(X, y)

    joblib.dump(final_model, MODEL_PATH)
    print(f"\nModel yadda saxlanıldı: {MODEL_PATH}")


if __name__ == "__main__":
    main()
