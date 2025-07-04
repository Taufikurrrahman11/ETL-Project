import pytest
import pandas as pd
from utils.transform import transform_data

def test_transform():
    df = pd.DataFrame([{
        'Title': 'Shirt',
        'Price': '$100',
        'Rating': '4.5 / 5',
        'Colors': '3 Colors',
        'Size': 'Size: L',
        'Gender': 'Gender: Men',
        'Timestamp': '2025-05-10'
    }])
    df = transform_data(df)
    assert df['Price'].iloc[0] == 1600000
    assert df['Rating'].iloc[0] == 4.5
    assert df['Colors'].iloc[0] == 3
