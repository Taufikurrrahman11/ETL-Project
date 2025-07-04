
# test_load.py
import pandas as pd
import os
from etl.load import load_csv

def test_load_csv():
    test_path = 'data/test_output.csv'
    df = pd.DataFrame({"col1": [1], "col2": [2]})
    load_csv(df, test_path)
    assert os.path.exists(test_path)
    loaded_df = pd.read_csv(test_path)
    assert not loaded_df.empty
    os.remove(test_path)
