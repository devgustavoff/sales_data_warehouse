import pandas as pd
import os

def extract():
    df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "superstore_sales.csv"), encoding="latin-1")

    return df