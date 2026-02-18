import pandas as pd

def load_movies(csv_path: str):
    df = pd.read_csv(csv_path)
    return df
