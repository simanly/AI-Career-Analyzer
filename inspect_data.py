
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent

datasets = {
    "Test Profiles": (
        BASE_DIR / "data" / "raw" / "profiles_test.csv",
        "career_class"
    ),
    "Real Resumes": (
        BASE_DIR / "data" / "raw" / "resumes_real.csv",
        "category"
    ),
    "Job Vacancies": (
        BASE_DIR / "vacancies_clean.csv",
        "job_group"
    ),
}

for name, (path, target) in datasets.items():
    print("\n" + "=" * 50)
    print("DATASET:", name)
    print("=" * 50)

    if not path.exists():
        print("FAYL TAPILMADI:", path)
        continue

    df = pd.read_csv(path)

    print("Ölçü:", df.shape)
    print("Sütunlar:", df.columns.tolist())
    print("Hədəf sütunu:", target)

    if target in df.columns:
        print("Hədəf sütunundakı boş dəyərlər:", df[target].isna().sum())
        print("Sinif sayı:", df[target].nunique())
        print("Sinif bölgüsü:")
        print(df[target].value_counts(dropna=False).to_string())
    else:
        print("XƏBƏRDARLIQ: Hədəf sütunu tapılmadı!")

    print("\nBoş dəyərlər:")
    print(df.isna().sum().to_string())
    
    print("\nİlk 2 sətrin qısa görünüşü:")
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype("string").str.slice(0, 100)

    print(df.head(2).to_string(index=False))
