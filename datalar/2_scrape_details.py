# Step 2: open every vacancy link and collect more columns.
# It saves progress, so you can stop and run again.
import requests, pandas as pd, json, re, time, os
from bs4 import BeautifulSoup

H = {"User-Agent": "Mozilla/5.0"}
IN, OUT = "hellojob_150_sehife.csv", "hellojob_details.csv"

# label on the site -> our column name (add more if you see more labels)
LABELS = {
    "Kateqoriya": "category", "Şəhər": "city", "Maaş": "salary",
    "Təhsil": "education", "Təcrübə": "experience", "İş rejimi": "job_type",
    "Yaş": "age", "Elanın tarixi": "posted_date", "Bitmə tarixi": "deadline",
    "Yerləşdirilib": "posted_date", "Son tarix": "deadline",
}

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    row = {}
    # 1) JSON-LD (many sites have it)
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(tag.string or "")
        except Exception:
            continue
        d = d[0] if isinstance(d, list) and d else d
        if isinstance(d, dict) and d.get("@type") == "JobPosting":
            row["description"] = BeautifulSoup(d.get("description", ""), "html.parser").get_text(" ", strip=True)
            row["posted_date"] = d.get("datePosted")
            row["deadline"] = d.get("validThrough")
            loc = d.get("jobLocation")
            loc = loc[0] if isinstance(loc, list) and loc else loc
            if isinstance(loc, dict):
                row["city"] = (loc.get("address") or {}).get("addressLocality")
    # 2) label -> next line in page text
    lines = [l.strip() for l in soup.get_text("\n").split("\n") if l.strip()]
    for i, line in enumerate(lines[:-1]):
        key = line.rstrip(":").strip()
        if key in LABELS and LABELS[key] not in row:
            row[LABELS[key]] = lines[i + 1]
    # 3) description = longest text block, if still empty
    if not row.get("description"):
        blocks = [b.get_text(" ", strip=True) for b in soup.find_all(["div", "section"])]
        row["description"] = max(blocks, key=len)[:6000] if blocks else ""
    h1 = soup.find("h1")
    row["title"] = h1.get_text(" ", strip=True) if h1 else None
    return row

df_full = pd.read_csv(IN)
df = df_full.sample(n=1000, random_state=42)
done = pd.read_csv(OUT) if os.path.exists(OUT) else pd.DataFrame(columns=["Link"])
todo = df[~df["Link"].isin(done["Link"])]
rows = done.to_dict("records")

for n, url in enumerate(todo["Link"], 1):
    try:
        r = requests.get(url, headers=H, timeout=15)
        data = parse(r.text) if r.status_code == 200 else {"error": r.status_code}
    except Exception as e:
        data = {"error": str(e)[:50]}
    data["Link"] = url
    rows.append(data)
    if n % 50 == 0:
        pd.DataFrame(rows).to_csv(OUT, index=False, encoding="utf-8-sig")
        print(n, "/", len(todo))
    time.sleep(1)

pd.DataFrame(rows).to_csv(OUT, index=False, encoding="utf-8-sig")
print("Done:", len(rows), "rows")