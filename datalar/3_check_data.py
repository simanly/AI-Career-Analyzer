import pandas as pd

# 1. Load the scraped data
df = pd.read_csv("hellojob_details.csv")

print("Dataset shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

# 2. Check missing values
print("\nMissing values:")
print(df.isna().sum())

# 3. Check duplicate links
print("\nDuplicate links:", df["Link"].duplicated().sum())

# 4. Check description lengths
df["description"] = df["description"].fillna("").astype(str)

df["description_length"] = df["description"].str.len()

print("\nDescription length statistics:")
print(df["description_length"].describe())

print(
    "\nDescriptions shorter than 200 characters:",
    (df["description_length"] < 200).sum()
)

# 5. Check categories
print("\nTop 20 categories:")
print(df["category"].value_counts().head(20))

# 6. Check scraping errors
if "error" in df.columns:
    print("\nScraping errors:", df["error"].notna().sum())

# 7. Inspect a few descriptions
for i, description in enumerate(df["description"].head(3), start=1):
    print(f"\n--- Description {i} ---")
    print(description[:700])

# 8. Check whether important fields are empty
print("\nEmpty titles:", df["title"].isna().sum())
print("Empty descriptions:", (df["description"].str.strip() == "").sum())