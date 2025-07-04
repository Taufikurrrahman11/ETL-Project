from utils.extract import extract_all
from utils.transform import transform_data
from utils.load import load_csv, load_google_sheets, load_postgres

if __name__ == "__main__":
    try:
        print("Extracting data...")
        raw_df = extract_all()
    except Exception as e:
        print(f"Error during extraction: {e}")
        exit(1)

    try:
        print("Transforming data...")
        clean_df = transform_data(raw_df)
    except Exception as e:
        print(f"Error during transformation: {e}")
        exit(1)

    try:
        print("Loading data to CSV...")
        load_csv(clean_df)
        print("Loading data to Google Sheets...")
        load_google_sheets(clean_df)
        print("Loading data to PostgreSQL...")
        load_postgres(clean_df)
    except Exception as e:
        print(f"Error during loading: {e}")
        exit(1)

    print("ETL process completed successfully.")