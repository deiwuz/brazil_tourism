import pandas as pd
from pathlib import Path
from datetime import datetime
from functools import wraps
import sys

def logs(func):
    """
    Decorator to log the execution time of a function.
    
    Args:
        func (callable): The function to be decorated.
        
    Returns:
        callable: The wrapped function with logging.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Processing {func.__name__} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return func(*args, **kwargs)
    return wrapper

def standardize_headers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column headers.

    Converts headers to lowercase, strips whitespace, and translates
    Portuguese headers to English.

    Args:
        df (pd.DataFrame): Input DataFrame with raw headers.

    Returns:
        pd.DataFrame: DataFrame with standardized English headers.
    """
    df.columns = df.columns.str.lower().str.strip()

    headers = {
        "continente": "continent",
        "cod continente": "continent_code",
        "país": "country",
        "cod pais": "country_code",
        "uf": "state",
        "cod uf": "state_code",
        "via": "via",
        "cod via": "via_code",
        "ano": "year",
        "mês": "month",
        "cod mes": "month_code",
        "chegadas": "arrivals",
    }
    
    df = df.rename(columns=headers)
    return df

def strip_whitespace(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip leading and trailing whitespace from all string columns.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with whitespace stripped from object columns.
    """
    for col in df.select_dtypes(include=[object]).columns:
        df[col] = df[col].str.strip()

    return df

def verify_nan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values in the DataFrame.

    Specifically, fills missing values in the 'arrivals' column with 0.

    Args:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame with NaN values handled.
    """
    df['arrivals'] = df['arrivals'].fillna(0)
    return df

@logs
def clean_data(sys_argv: list) -> pd.DataFrame:
    """
    Main function to drive the data cleaning process.

    Reads raw data, applies standardization, cleaning, handles missing values,
    adds processing metadata, and saves the result to a CSV file.

    Args:
        sys_argv (list): List of command line arguments.
                        - sys_argv[1]: (Optional) Path to raw input file.
                        - sys_argv[2]: (Optional) Path to output cleaned file.
                        Defaults are used if arguments are not provided.

    Returns:
        pd.DataFrame: The cleaned pandas DataFrame.
    """
    print("="*60)
    print("STEP 1: Data Cleaning")
    print("="*60)
    print("DEBUG - Inicio del script")
    print(f"DEBUG - Argumentos totales recibidos: {len(sys.argv)}")
    print(f"DEBUG - Lista completa de argumentos: {sys.argv}")
    
    if len(sys_argv) >= 3:
        data_path = sys_argv[1]
        output_path = sys_argv[2]
        print("="*60)
        print(f"El sistema ha tomado como argumento el archivo {data_path}")
        print("="*60)
    else:
        data_path = Path("./raw/chegadas_2024.csv")
        output_path = Path("./clean/clean_visitors.csv")
        print("="*60)
        print(f"Ningun argumento ha sido ingresado, por lo que se tomara el archivo {data_path}")
        print("="*60)
    
    df = pd.read_csv(data_path, encoding="iso-8859-1", sep=";", dtype_backend='numpy_nullable')
    df = standardize_headers(df)
    df = strip_whitespace(df)
    df = verify_nan(df)
    df['processed_at'] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%d %H:%M:%S")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Data cleaned and saved to {output_path}")
    return df

if __name__ == "__main__":
    clean_data(sys_argv)
