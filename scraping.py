import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Saytın ünvanı və Headers (Saytın sorğunu bot kimi bloklamaması üçün)
url = "https://www.hellojob.az/vakansiyalar"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Məlumatlar çəkilir...")
# 2. HTTP GET sorğusu göndəririk
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # 3. HTML məzmununu BeautifulSoup vasitəsilə parse edirik
    soup = BeautifulSoup(response.text, "html.parser")
    
    vacancies_data = []
    
    # 4. Vakansiya bloklarını tapırıq
    items = soup.find_all("a", class_="vacancies__item") or soup.select(".vacancy_item, .vacancies__item")
    
    for item in items:
        # Vakansiya başlığı
        title_elem = item.find("h3") or item.find(class_="vacancies__item-title") or item.find("p")
        title = title_elem.text.strip() if title_elem else "N/A"
        
        # Şirkət adı
        company_elem = item.find(class_="vacancies__item-company") or item.find("span")
        company = company_elem.text.strip() if company_elem else "N/A"
        
        # Vakansiya haqqında ətraflı keçid (URL)
        link = item.get("href", "")
        if link and not link.startswith("http"):
            link = "https://www.hellojob.az" + link
            
        vacancies_data.append({
            "Vakansiya": title,
            "Şirkət": company,
            "Link": link
        })
    
    # 5. Məlumatları Pandas DataFrame-ə çeviririk və CSV faylı kimi saxlayırıq
    df = pd.DataFrame(vacancies_data)
    df.to_csv("hellojob_vacancies.csv", index=False, encoding="utf-8-sig")
    
    print(f"Uğurla {len(vacancies_data)} vakansiya toplandı və 'hellojob_vacancies.csv' faylına yazıldı!")
else:
    print(f"Xəta baş verdi! Status kodu: {response.status_code}")