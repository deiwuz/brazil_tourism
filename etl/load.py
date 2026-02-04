from sqlalchemy import create_engine, types
import pandas as pd
from airflow.hooks.base import BaseHook

schema_map = {
    "continent": types.String(50),
    "continent_code": types.Integer(),
    "country": types.String(50),
    "country_code": types.Integer(),
    "state": types.String(50),
    "state_code": types.Integer(),
    "via": types.String(50),
    "via_code": types.Integer(),
    "year": types.Integer(),
    "month": types.String(50),
    "month_code": types.Integer(),
    "arrivals": types.Integer(),
    "processed_at": types.DateTime(),
}

def get_db_connection():
    """
    Establish a connection to the Postgres database.
    
    Uses Airflow's BaseHook to retrieve connection details configured
    in the Airflow environment (AIRFLOW_CONN_POSTGRES_BRAZIL_ETL).
    
    Returns:
        sqlalchemy.engine.Engine: A SQLAlchemy engine instance connected to the database.
    """
    # this url uses the airflow user and password to connect to the postgres container, these were set on the docker-compose.airflow.yaml file
    connection = BaseHook.get_connection("postgres_brazil_etl")

    db_url = connection.get_uri()

    engine = create_engine(db_url)

    return engine

def csv_to_sql(df: pd.DataFrame, engine: create_engine):
    """
    Load the DataFrame into the Postgres database.
    
    Replaces the table 'clean_visitors' if it exists.
    
    Args:
        df (pd.DataFrame): The DataFrame to load.
        engine (sqlalchemy.engine.Engine): The database engine.
    """
    df.to_sql('clean_visitors', engine, if_exists='replace', index=False, dtype=schema_map)


def load_data(df: pd.DataFrame):
    """
    Main function to drive the data loading process.
    
    Establishes a database connection and loads the provided DataFrame
    into the 'clean_visitors' table.
    
    Args:
        df (pd.DataFrame): The DataFrame to be loaded.
    """
    engine = get_db_connection()

    csv_to_sql(df, engine)
