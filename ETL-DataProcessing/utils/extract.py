import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

BASE_URL = 'https://fashion-studio.dicoding.dev'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0 Safari/537.36'
}

def scrape_page(page):
    if page == 1:
        url = BASE_URL + '/'
    else:
        url = f"{BASE_URL}/page{page}"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Error fetching page {page}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', class_='collection-card')
    print(f"🔎 Ditemukan {len(items)} item di page {page}")

    result = []
    for item in items:
        title = item.find('h3').text.strip() if item.find('h3') else None

        # Tangani dua kemungkinan struktur HTML untuk harga
        price_tag = item.select_one('div.price-container span.price') or item.select_one('p.price')
        price = price_tag.get_text(strip=True) if price_tag else None

        # Tangani elemen lainnya secara aman
        rating = item.find('p', string=lambda s: s and "Rating" in s)
        colors = item.find('p', string=lambda s: s and "Colors" in s)
        size = item.find('p', string=lambda s: s and "Size" in s)
        gender = item.find('p', string=lambda s: s and "Gender" in s)

        result.append({
            'Title': title,
            'Price': price,
            'Rating': rating.get_text(strip=True) if rating else None,
            'Colors': colors.get_text(strip=True) if colors else None,
            'Size': size.get_text(strip=True) if size else None,
            'Gender': gender.get_text(strip=True) if gender else None,
            'Timestamp': datetime.now()
        })
    return result

def extract_all():
    all_data = []
    for page in range(1, 51):
        print(f"🔍 Extracting page {page}...")
        data = scrape_page(page)
        all_data.extend(data)
        time.sleep(2)  # Hindari diblokir server
    return pd.DataFrame(all_data)
