"""
Brazilian Tourism ETL Pipeline Package

This package provides a pipeline for processing Brazilian tourism data.
It currently supports cleaning and standardizing raw arrival data.

Pipeline Overview:
    1. Standardize headers (Portuguese to English)
    2. Strip whitespace from text columns
    3. Handle missing values (NaN)
    4. Save processed data
    5. Load data into Postgres database

Key Features:
    - Translation of column names from Portuguese to English
    - Robust data cleaning
    - Execution logging

Modules:
    clean: Data cleaning and standardization functions

Exported Functions:
    clean_data: Main entry point for the cleaning pipeline

Usage Examples:
    # Import the cleaning function
    from etl import clean_data

    # Run cleaning pipeline with default paths
    df = clean_data()

    # Or specify custom input/output paths
    # df = clean_data(["raw_data.csv", "clean_data.csv"])

Requirements:
    - pandas
    - pathlib
    - datetime

Version: 0.1.0
Author: Deiwuz
"""

__version__ = "0.1.0"

from .clean import clean_data
from .load import load_data

__all__ = [
    'clean_data',
    'load_data'
]