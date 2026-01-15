from numpy import number
import pandas as pd
from pathlib import Path
from datetime import datetime
from functools import wraps

data_path = Path("./data/chegadas_2024.csv")
output_path = Path("./data/clean_visitors.csv")

def logs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Processing {func.__name__} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return func(*args, **kwargs)
    return wrapper

def standardize_headers(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = df.columns.str.lower().str.strip()

    headers = {
        "continente": "Continent",
        "cod continente": "Continent Code",
        "país": "Country",
        "cod pais": "Country Code",
        "uf": "State",
        "cod uf": "State Code",
        "via": "Via",
        "cod via": "Via Code",
        "ano": "Year",
        "mês": "Month",
        "cod mes": "Month Code",
        "chegadas": "Arrivals",
    }
    
    df = df.rename(columns=headers)
    return df

def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    for col in df.select_dtypes(include=[object]).columns:
        df[col] = df[col].str.strip()

    return df

def verify_nan(df: pd.DataFrame) -> pd.DataFrame:
    df['Arrivals'] = df['Arrivals'].fillna(0)
    return df

@logs
def clean_data():
    df = pd.read_csv(data_path, encoding="iso-8859-1", sep=";", dtype_backend='numpy_nullable')
    df = standardize_headers(df)
    df = strip_whitespace(df)
    df = verify_nan(df)
    df['processed_at'] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(output_path, index=False, encoding="utf-8")

if __name__ == "__main__":
    clean_data()
