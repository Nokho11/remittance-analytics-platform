from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

FILES_DIR = "/Users/NOKHO/remittance-analytics-platform/scripts"
DBT_DIR = "/Users/NOKHO/remittance-analytics-platform/dbt_pipeline"
PYTHON_BASE = "/opt/anaconda3/bin/python3"
DBT_BIN = "/Users/NOKHO/dbt_env/bin/dbt"

with DAG(
    dag_id="pipeline_marches",
    start_date=datetime(2026, 8, 1),
    schedule="0 7 * * 1-5",
    catchup=False,
) as dag:

    extract_yfinance = BashOperator(
        task_id="extract_yfinance",
        bash_command=f'cd "{FILES_DIR}" && "{PYTHON_BASE}" extraction_yfinance.py',
    )

    extract_frankfurter = BashOperator(
        task_id="extract_frankfurter",
        bash_command=f'cd "{FILES_DIR}" && "{PYTHON_BASE}" extraction_frankfurter.py',
    )

    extract_worldbank = BashOperator(
        task_id="extract_worldbank",
        bash_command=f'cd "{FILES_DIR}" && "{PYTHON_BASE}" extraction_worldbank.py',
    )

    load_bigquery = BashOperator(
        task_id="load_bigquery",
        bash_command=f'cd "{FILES_DIR}" && "{PYTHON_BASE}" chargement_bigquery.py',
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f'cd "{DBT_DIR}" && "{DBT_BIN}" run',
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f'cd "{DBT_DIR}" && "{DBT_BIN}" test',
    )

    [extract_yfinance, extract_frankfurter, extract_worldbank] >> load_bigquery >> dbt_run >> dbt_test
