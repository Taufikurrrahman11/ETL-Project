import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def load_csv(df, path='restoran_data.csv'):
    df.to_csv(path, index=False)
    print(f"✅ Data disimpan sebagai CSV di {path}")

def load_google_sheets(df):
    if df.empty:
        print("⚠️ Data kosong, tidak dikirim ke Google Sheets.")
        return

    if not os.path.exists('google-sheets-api.json'):
        print("❌ File google-sheets-api.json tidak ditemukan.")
        return

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('google-sheets-api.json', scope)
        client = gspread.authorize(creds)

        sheet = client.create("Data Restoran PergiKuliner")
        sheet.share(None, perm_type='anyone', role='writer')
        worksheet = sheet.sheet1
        worksheet.append_rows([df.columns.tolist()] + df.values.tolist())

        print("✅ Data berhasil dikirim ke Google Sheets.")
    except Exception as e:
        print(f"❌ Gagal upload ke Google Sheets: {e}")

def load_postgres(df):
    db_url = os.getenv("POSTGRES_URI")
    if not db_url:
        print("❌ POSTGRES_URI belum diset di file .env")
        return

    try:
        engine = create_engine(db_url)
        df.to_sql("restoran_jakarta", engine, if_exists='replace', index=False)
        print("✅ Data berhasil dikirim ke PostgreSQL.")
    except Exception as e:
        print(f"❌ Gagal koneksi ke PostgreSQL: {e}")
