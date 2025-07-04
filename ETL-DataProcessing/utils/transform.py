import pandas as pd
import re
from datetime import datetime

EXCHANGE_RATE = 16000  # 1 USD to IDR
INVALID_VALUES = ["", "none", "null", "na", "n/a", "invalid", "not rated", "unavailable", "-", "unknown"]

def is_invalid(value):
    return pd.isna(value) or str(value).strip().lower() in INVALID_VALUES

def clean_price(price):
    if is_invalid(price):
        return None  # Tandai invalid
    try:
        price_clean = pd.to_numeric(str(price).replace('$', '').replace(',', '').strip(), errors='coerce')
        return int(price_clean * EXCHANGE_RATE) if pd.notnull(price_clean) else None
    except Exception:
        return None

def clean_rating(rating):
    if is_invalid(rating):
        return None
    try:
        match = re.search(r'(\d+(\.\d+)?)', str(rating))
        return round(float(match.group(1)), 1) if match else None
    except Exception:
        return None

def clean_colors(colors):
    if is_invalid(colors):
        return None
    try:
        match = re.search(r'\d+', str(colors))
        return int(match.group()) if match else None
    except Exception:
        return None

def clean_size(size):
    if is_invalid(size):
        return None
    return str(size).replace("Size:", "").strip().upper()

def clean_gender(gender):
    if is_invalid(gender):
        return None
    return str(gender).replace("Gender:", "").strip().capitalize()

def clean_title(title):
    if is_invalid(title) or str(title).strip() == "Unknown Product":
        return None
    return title

def transform_data(df):
    df['Title'] = df['Title'].apply(clean_title)
    df['Price'] = df['Price'].apply(clean_price)
    df['Rating'] = df['Rating'].apply(clean_rating)
    df['Colors'] = df['Colors'].apply(clean_colors)
    df['Size'] = df['Size'].apply(clean_size)
    df['Gender'] = df['Gender'].apply(clean_gender)
    df['Timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Hapus baris yang masih mengandung data None setelah dibersihkan
    df_cleaned = df.dropna(subset=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'])

    # Susun kolom sesuai urutan yang diharapkan
    desired_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender', 'Timestamp']
    return df_cleaned[desired_columns]
