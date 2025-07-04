import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def load_csv(df, path='product.csv'):
    df.to_csv(path, index=False)

def load_google_sheets(df):
    if df.empty:
        print("DataFrame kosong, tidak dapat memuat ke Google Sheets.")
        return

    if not os.path.exists('google-sheets-api.json'):
        print("File kredensial Google Sheets tidak ditemukan.")
        return

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('google-sheets-api.json', scope)
    client = gspread.authorize(creds)
    sheet = client.create("ETL Cleaned Data")
    sheet.share(None, perm_type='anyone', role='writer')
    worksheet = sheet.get_worksheet(0)
    worksheet.insert_rows([df.columns.tolist()] + df.values.tolist())

def load_postgres(df):
    db_url = os.getenv("POSTGRES_URI")  # ganti dari DATABASE_URL
    engine = create_engine(db_url)
    df.to_sql("fashion_data", engine, if_exists='replace', index=False)