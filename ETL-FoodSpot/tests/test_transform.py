# test_transform.py
import pytest
import pandas as pd
from etl.transform import transform_data

def test_transform():
    df = pd.DataFrame([{
        'Nama Restoran': 'Test Resto',
        'Jenis Makanan': 'Jepang',
        'Alamat': 'Jl. Test No. 1',
        'Jam Buka': '10:00 - 22:00',
        'Telepon': '08123456789',
        'Harga': 'Rp. 50.000 - Rp. 100.000',
        'Rating': '4.2'
    }])
    clean_df = transform_data(df)
    assert clean_df['Rating'].dtype == float
    assert clean_df['Harga'].str.contains("Rp").any() == False  # Sudah dibersihkan
    assert ' - ' not in clean_df['Harga'].iloc[0]  # Sudah dirata-rata atau disederhanakan