"""
Entry point for the Brazilian Tourism ETL Pipeline.

This module orchestrates the execution of the ETL pipeline steps:
1. Data Cleaning
2. Data Loading
"""
from etl import clean_data, load_data
import sys

def main(sys_argv: list) -> None:
    """
    Execute the complete Brazilian ETL pipeline.

    This function sequentially runs the following steps:
    1. Data Cleaning: Processes raw data and saves it.
    2. Data Loading: Loads the processed data into the database.

    Args:
        sys_argv (list): Command line arguments passed to the script.
                        First argument is script name, followed by inputs.
                        See `etl.clean.clean_data` for specific argument usage.

    Returns:
        None
    """
    
    print("="*60)
    print("Welcome to your Brazilian ETL Pipeline!")
    print("="*60)
    
    # Step 1: Explore and load data
    df = clean_data(sys.argv)

    load_data(df)

if __name__ == "__main__":
    main(sys.argv)
