from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

PROJECT_DIR = "C:/Users/user/Desktop/Personal/Data Science Github/PSI-Engine-Automated-Risk-Detection-Inventory-Optimization"
DBT_BIN = "C:/Users/user/Desktop/Personal/Data Science Github/PSI-Engine-Automated-Risk-Detection-Inventory-Optimization/venv/Scripts/dbt.exe"
PYTHON_BIN = "python"

# Default arguments for the pipeline
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'supply_chain_control_tower',
    default_args=default_args,
    description='Orchestrates dbt transformations and CSV export for PSI Dashboard',
    schedule_interval=None, # Set to '@daily' for production
    start_date=datetime(2026, 2, 1),
    catchup=False,
    tags=['supply_chain', 'dbt', 'pii_governance'],
) as dag:

    # Task 1: Run dbt (Builds models, runs tests, shifts dates, and hashes PII)
    # We point explicitly to the project and profiles directories
    t1_dbt_run = BashOperator(
        task_id='dbt_build_all',
        bash_command=(
            f'{DBT_BIN} build '
            f'--project-dir {PROJECT_DIR}/dbt_project '
            f'--profiles-dir {PROJECT_DIR}/dbt_project'
        ),
    )

    # Task 2: Export for Power BI
    # This task only triggers if t1 (dbt tests) passes perfectly
    t2_export_data = BashOperator(
        task_id='export_to_powerbi',
        bash_command=f'{PYTHON_BIN} {PROJECT_DIR}/scripts/export_data.py',
    )

    # Setting the dependency
    t1_dbt_run >> t2_export_data