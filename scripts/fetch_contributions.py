import requests
from bs4 import BeautifulSoup
import json
import os

# GitHub'ın herkese açık katkı takvimi arayüzü
url = "https://github.com/users/alibahadiruyumaz/contributions"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
days = soup.find_all('td', class_='ContributionCalendar-day')

data = []
for day in days:
    if 'data-date' in day.attrs:
        data.append({"date": day['data-date'], "level": day.get('data-level', 0)})

os.makedirs("data", exist_ok=True)
with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(data, f)
    
print("Katkı verileri başarıyla data/contributions.json dosyasına kaydedildi.")