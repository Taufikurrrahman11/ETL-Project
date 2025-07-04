import pandas as pd
from utils.load import load_csv
import os

def test_load_csv():
    path = 'data/test_output.csv'
    df = pd.DataFrame({"col1": [1], "col2": [2]})
    load_csv(df, path)
    assert os.path.exists(path)
    os.remove(path)