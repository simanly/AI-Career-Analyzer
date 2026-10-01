import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

base_url = "https://www.hellojob.az/vakansiyalar?page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

all_data = []
target_pages = 150  # Scraping ediləcək səhifə sayısı

for page in range(1, target_pages + 1):
    url = f"{base_url}{page}"
    print(f"Səhifə {page}/{target_pages} çəkilir...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(f"Səhifə {page} yüklənərkən xəta baş verdi: {e}")
        continue
        
    if response.status_code != 200:
        print(f"Səhifə {page} açıla bilmədi. Status kodu: {response.status_code}")
        continue
        
    soup = BeautifulSoup(response.text, "html.parser")
    vacancies = soup.find_all("div", class_="vacancies__item")
    
    # Əgər saytda ümumi səhifə sayı 150-dən azdırsa və vakansiya bitibsə dövrü dayandırır
    if not vacancies:
        print(f"Səhifə {page}-də vakansiya tapılmadı. Proses tez tamamlandı.")
        break
        
    for item in vacancies:
        link_elem = item.find("a", class_="vacancies__body")
        link = link_elem["href"] if link_elem and "href" in link_elem.attrs else ""
        
        content = item.find("div", class_="vacancies__content")
        
        if content:
            title_elem = content.find("h3") or content.find("p") or content.find("div")
            title = title_elem.text.strip() if title_elem else "N/A"
            
            company_elem = content.find("span")
            company = company_elem.text.strip() if company_elem else "N/A"
            
            all_data.append({
                "Vakansiya adı": title,
                "Şirkət": company,
                "Link": link
            })
    
    # Serverin IP unvanınızı bloklamaması üçün hər səhifə arası 1 saniyə pauza
    time.sleep(1)

# Bütün məlumatları CSV faylına yazırıq
df = pd.DataFrame(all_data)
df.to_csv("hellojob_150_sehife.csv", index=False, encoding="utf-8-sig")

print(f"\nProses tamamlandı! Ümumilikdə {len(all_data)} vakansiya toplandı və 'hellojob_150_sehife.csv' faylına yazıldı.")