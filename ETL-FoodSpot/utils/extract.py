import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def extract_all():
    base_url = "https://pergikuliner.com/restoran/jakarta/?page="
    total_pages = 125
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    data = []

    for page in range(1, total_pages + 1):
        print(f"📄 Memuat halaman {page}...")
        driver.get(f"{base_url}{page}")
        time.sleep(2)

        restaurants = driver.find_elements(By.CLASS_NAME, "restaurant-result-wrapper")
        for resto in restaurants:
            try:
                name = resto.find_element(By.CLASS_NAME, "item-name").text.strip()

                group_text = resto.find_element(By.CLASS_NAME, "item-group").text.strip()
                cuisine = group_text.split("|")[1].strip() if "|" in group_text else None

                # Alamat
                address = None
                clearfix_elements = resto.find_elements(By.CLASS_NAME, "clearfix")
                for el in clearfix_elements:
                    if 'icon-map' in el.get_attribute('innerHTML'):
                        address = el.text.strip()
                        break

                # Harga
                price = None
                for el in clearfix_elements:
                    if 'icon-price' in el.get_attribute('innerHTML'):
                        price = el.text.strip()
                        break

                rating = resto.find_element(By.CLASS_NAME, "item-rating-result").text.strip()

                data.append({
                    "Nama Restoran": name,
                    "Jenis Makanan": cuisine,
                    "Alamat": address,
                    "Harga": price,
                    "Rating": rating,
                    "Timestamp": pd.Timestamp.now()
                })

            except Exception as e:
                print(f"❌ Gagal ekstrak 1 data: {e}")

    driver.quit()
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = extract_all()
    print(f"✅ Ekstraksi selesai. Total data: {len(df)}")
    df.to_csv("restoran_data.csv", index=False)
    print("✅ Data disimpan ke restoran_data.csv.")
