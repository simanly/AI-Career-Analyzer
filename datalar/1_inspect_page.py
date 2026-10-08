# Step 1: save ONE vacancy page, so we can see the real HTML.
import requests, pandas as pd
H = {"User-Agent": "Mozilla/5.0"}
url = pd.read_csv("hellojob_150_sehife.csv")["Link"].iloc[0]
html = requests.get(url, headers=H, timeout=15).text
open("sample_vacancy.html", "w", encoding="utf-8").write(html)
print(url, len(html), "chars saved to sample_vacancy.html")
 