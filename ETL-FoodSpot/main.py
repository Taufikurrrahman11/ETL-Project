from src.etl.extract import extract_all
from src.etl.transform import transform_data
from src.etl.load import load_csv, load_google_sheets, load_postgres
from src.preprocessing.preprocess import preprocess_data
from src.models.train_model import train_model
from src.recommend.recommend import rekomendasi_resto

def main():
    print("🚀 Memulai proses ETL PergiKuliner...")

    # Extract
    try:
        print("📥 Extracting data dari web...")
        raw_df = extract_all()
        if raw_df.empty:
            print("⚠️ Tidak ada data yang berhasil diambil.")
            return
        print(f"✅ Berhasil mengekstrak {len(raw_df)} data.")
    except Exception as e:
        print(f"❌ Error saat proses ekstraksi: {e}")
        return

    # Transform
    try:
        print("🔧 Transforming data...")
        clean_df = transform_data(raw_df)
        print(f"✅ Data setelah transformasi: {len(clean_df)} baris.")
    except Exception as e:
        print(f"❌ Error saat proses transformasi: {e}")
        return

    # Load
    try:
        print("💾 Menyimpan data ke CSV...")
        load_csv(clean_df)

        print("📤 Mengunggah data ke Google Sheets...")
        load_google_sheets(clean_df)

        print("🛢️ Mengirim data ke PostgreSQL...")
        load_postgres(clean_df)

        print("🎉 ETL PergiKuliner selesai dengan sukses!")
    except Exception as e:
        print(f"❌ Error saat proses load: {e}")
        return

    # Preprocessing
    try:
        print("🧹 Memproses data untuk model...")
        preprocess_data('data/raw/restoran_data.csv', 'data/processed/restoran_clean.csv')
    except Exception as e:
        print(f"❌ Error saat preprocessing: {e}")
        return

    # Train Model
    try:
        print("🧠 Melatih model rekomendasi...")
        train_model('data/processed/restoran_clean.csv')
    except Exception as e:
        print(f"❌ Error saat training model: {e}")
        return

    # Recommend Example
    try:
        print("🤖 Menampilkan rekomendasi contoh...")
        rekomendasi = rekomendasi_resto("The Social Pot")
        if rekomendasi is not None:
            print(rekomendasi)
    except Exception as e:
        print(f"❌ Error saat menjalankan rekomendasi: {e}")

if __name__ == "__main__":
    main()
