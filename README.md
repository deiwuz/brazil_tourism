# Brazilian Tourism ETL Pipeline

A Python-based ETL (Extract, Transform, Load) pipeline for processing Brazilian tourism arrival data. This project standardizes raw CSV data from the Ministry of Tourism, performing cleaning and translation of headers for easier analysis.

## Features

- **Standardization**: Converts Portuguese headers to English.
- **Data Cleaning**: Strips whitespace from string columns and handles missing values.
- **Traceability**: Adds a `processed_at` timestamp to every record.
- **Fast Development**: Powered by `uv` for dependency management.

## Project Structure

```text
Brazilian_etl/
├── etl/
│   ├── __init__.py        # Package initialization
│   ├── clean.py           # Standardization and cleaning of data
├── data/
│   ├── chegadas_2024.csv  # Raw data (ISO-8859-1)
│   └── clean_visitors.csv # Processed data (UTF-8)
├── main.py                # Entry point for data cleaning
├── pyproject.toml         # Project metadata and dependencies
└── README.md              # Project documentation
```

## Prerequisites

- **Python >= 3.11**: The project is built on Python 3.14.
- [uv](https://github.com/astral-sh/uv) (Recommended for dependency management)
- **Pyproject.toml**: Must contain the correct project dependencies.

## Configuration

The following environment variables are required for the project to function correctly, particularly for the Airflow and Postgres integration.

You can set these in a `.env` file or export them in your shell.

```bash
AIRFLOW_UID=1000
AIRFLOW_PROJ_DIR=/home/deiwuz/Documents/brazil_etl/airflow
POSTGRES_URI=postgresql+psycopg2://postgres:your_password@postgres-etl:5432/brazil_etl
AIRFLOW__SMTP__SMTP_EMAIL_BACKEND=airflow.utils.email.send_email_smtp
AIRFLOW__SMTP__SMTP_HOST=smtp.gmail.com
AIRFLOW__SMTP__SMTP_PORT=587
AIRFLOW__SMTP__SMTP_MAIL_FROM=user@example.com
AIRFLOW__SMTP__SMTP_STARTTLS=1
AIRFLOW__SMTP__SMTP_SSL=0
```

> [!IMPORTANT]
> Replace `your_password` and `user@example.com` with your actual secure credentials.

## Docker Compose Setup

For the full stack, including Airflow and Postgres, ensure your `docker-compose.yaml` (specifically for Airflow) includes the following configurations to map the environment variables and volumes correctly.

```yaml
    AIRFLOW_CONN_POSTGRES_BRAZIL_ETL: ${POSTGRES_URI}
  volumes:
    # --- Standard Airflow Mappings ---
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins

    # --- Custom Mappings ---
    - ../clean:/opt/airflow/clean # Clean csv output directory
    - ../raw:/opt/airflow/raw # Raw data directory
    - ../sql_snippets:/opt/airflow/sql_snippets # SQL snippets directory
    - ../main.py:/opt/airflow/main.py # Main script

volumes:
  postgres-db-volume:
  etl_data:
  metabase-data:

services:
  postgres-etl:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: your_password
      POSTGRES_DB: brazil_etl
    volumes:
      - etl_data:/var/lib/postgresql/data
    healthcheck:
      test: [ "CMD", "pg_isready", "-U", "postgres" ]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

  metabase:
    image: metabase/metabase:latest
    container_name: metabase
    ports:
      - "3000:3000"
    environment:
      MB_DB_FILE: /metabase-data/metabase.db
    volumes:
      - metabase-data:/metabase-data
    depends_on:
      - postgres-etl
```

## Setup

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Brazilian_etl
    ```

2.  **Install dependencies**:
    ```bash
    uv sync
    ```

## Usage

### Data Cleaning
To process the raw data and generate the cleaned output, run:
```bash
python etl/clean.py
```

## Data Information

- **Input**: `data/chegadas_2024.csv` (Encoded in `ISO-8859-1`, semicolon separator).
- **Transformations**:
  - Renames columns (e.g., `País` -> `Country`, `Chegadas` -> `Arrivals`).
  - Fills missing `Arrivals` with `0`.
  - Strips leading/trailing whitespace from categorical data.
  - Adds column `processed_at` with the current timestamp.
- **Output**: `data/clean_visitors.csv` (Encoded in `UTF-8`, standard comma separator).

## Author

**Deiwuz**
Version: 0.0.1