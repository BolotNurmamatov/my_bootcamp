"""Данный проект сохраняет университеты в формате csv"""

import os

import requests
import pandas as pd
import json
import csv
from datetime import datetime

# Создаем папку tmp в нашем проекте
os.makedirs("tmp", exist_ok=True)

file_path = os.path.join("tmp", "universities.csv")

# Выбираем страны для которых хотим получить список университетов
countries = ["Russia", "Belarus", "Kazakhstan", "Kyrgyzstan", "Turkey"]

# Инициализируем пусток список, чтобы хранить словари с информацией для каждого университета
all_universities = []

# Проходимся по каждой стране и сохраняем данные каждого университета
for country in countries:
    url = f"http://universities.hipolabs.com/search?name={country}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for uni in data:
            all_universities.append({
                "country": uni.get("country"),
                "name": uni.get("name"),
                "alpha_two_code": uni.get("alpha_two_code"),
                "state_province": uni.get("state-province"),
                "domain": ", ".join(uni.get("domains", [])),
                "web_page": ", ".join(uni.get("web_pages", [])),
                "updated_at": datetime.now().isoformat() 
            })
    else:
        print(f"Failed to fetch universities for {country}")

# Сохраняем в tmp папку в формате csv
with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_universities)

print(f"Saved to {file_path}")