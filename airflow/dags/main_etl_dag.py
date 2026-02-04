from datetime import datetime, timedelta
from typing import Any, Dict
import os

from airflow.sdk import dag
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

RAW_PATH: str = "/opt/airflow/raw/chegadas_2024.csv"
CLEAN_PATH: str = "/opt/airflow/clean/clean_chegadas_2024.csv"


default_args: Dict[str, Any] = {
    "owner": "airflow",
    "email": ["deiwuz4@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

@dag(schedule="0 2 * * 1",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args,)

def brazil_daily_etl():
    
    wait_file = FileSensor(
        task_id="wait_file",
        filepath=RAW_PATH,
        poke_interval=60,
        mode="reschedule",
        timeout=60*60,
        fs_conn_id="fs_brazil_etl"
    )
    run_etl = BashOperator(
        task_id="run_etl",
        cwd="/opt/airflow",
        retries=3,
        retry_delay=timedelta(minutes=2),
        env = {
            "AIRFLOW_HOME": "/opt/airflow",
            "PYTHONPATH": "/opt/airflow",
            "AIRFLOW_CONN_POSTGRES_BRAZIL_ETL": os.getenv("POSTGRES_URI")
        },
            
        bash_command=f"python3 /opt/airflow/main.py '{RAW_PATH}' '{CLEAN_PATH}'"
    )
    wait_file >> run_etl

brazil_daily_etl()
