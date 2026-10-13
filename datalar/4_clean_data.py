import pandas as pd
import re
import os

# Read the original dataset
df = pd.read_csv("hellojob_details.csv")

print("Original dataset:", df.shape)

# Remove rows with missing title or description
df["title"] = df["title"].fillna("").astype(str).str.strip()
df["description"] = df["description"].fillna("").astype(str).str.strip()

df = df[
    (df["title"] != "") &
    (df["description"].str.len() >= 200)
].copy()

# Clean extra spaces and line breaks
def clean_text(text):
    text = str(text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

df["title"] = df["title"].apply(clean_text)
df["description"] = df["description"].apply(clean_text)

# Remove duplicate links
df = df.drop_duplicates(subset=["Link"])

# Remove scraping-error rows if an error column exists
if "error" in df.columns:
    errors = df["error"].fillna("").astype(str).str.strip()
    df = df[errors == ""].copy()

# Save the cleaned dataset
os.makedirs("datalar/processed", exist_ok=True)

output_path = "datalar/processed/hellojob_cleaned.csv"
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nCleaned dataset:", df.shape)
print("Empty titles:", (df["title"] == "").sum())
print("Empty descriptions:", (df["description"] == "").sum())
print("Saved to:", output_path)