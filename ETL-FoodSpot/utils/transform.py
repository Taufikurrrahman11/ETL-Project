import pandas as pd
import re
from datetime import datetime

INVALID_VALUES = ["", "none", "null", "na", "n/a", "invalid", "not rated", "unavailable", "-", "unknown"]
ESSENTIAL_FIELDS = ['Nama Restoran']

def is_invalid(value):
    return pd.isna(value) or str(value).strip().lower() in INVALID_VALUES

def clean_text(value):
    return None if is_invalid(value) else str(value).strip()

def clean_rating(rating):
    if is_invalid(rating): 
        return None
    match = re.search(r'(\d+(\.\d+)?)', str(rating))
    return float(match.group(1)) if match else None

def clean_price(price):
    if is_invalid(price):
        return None
    try:
        angka = [int(re.sub(r'\D', '', p)) for p in re.findall(r'Rp\.?\s?[\d\.]+', price)]
        if "di atas" in price.lower() and angka:
            return angka[0]
        elif len(angka) == 2:
            return sum(angka) // 2
        elif len(angka) == 1:
            return angka[0]
        return None
    except Exception:
        return None

def transform_data(df):
    print("📊 Jumlah data awal:", len(df))

    df['Nama Restoran'] = df['Nama Restoran'].apply(clean_text)
    df['Jenis Makanan'] = df['Jenis Makanan'].apply(clean_text)
    df['Alamat'] = df['Alamat'].apply(clean_text)
    df['Harga'] = df['Harga'].apply(clean_price)
    df['Rating'] = df['Rating'].apply(clean_rating)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

    df = df.dropna(subset=ESSENTIAL_FIELDS)

    print("📉 Jumlah data setelah drop invalid:", len(df))

    return df[['Nama Restoran', 'Jenis Makanan', 'Alamat', 'Harga', 'Rating', 'Timestamp']]
