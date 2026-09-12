"""Illustrative Airflow DAG; connections must be configured outside source."""
from datetime import datetime, timedelta

try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
except ImportError:  # Allows repository inspection without Airflow installed.
    DAG = None


def extract(**context):
    print(f"Extract approved source for {context['ds']}")


def validate(**context):
    print(f"Run source checks for {context['ds']}")


def transform(**context):
    print(f"Build reporting grain for {context['ds']}")


def load(**context):
    print(f"Idempotently load partition {context['ds']}")


def refresh(**context):
    print("Trigger approved BI refresh connection")


if DAG:
    defaults = {
        "owner": "analytics",
        "retries": 2,
        "retry_delay": timedelta(minutes=5),
        "email_on_failure": True,
    }
    with DAG(
        dag_id="student_analytics_daily",
        start_date=datetime(2026, 1, 1),
        schedule="0 6 * * *",
        catchup=False,
        default_args=defaults,
        tags=["portfolio", "analytics"],
    ) as dag:
        extract_task = PythonOperator(task_id="extract", python_callable=extract)
        validate_task = PythonOperator(task_id="validate", python_callable=validate)
        transform_task = PythonOperator(task_id="transform", python_callable=transform)
        load_task = PythonOperator(task_id="load", python_callable=load)
        refresh_task = PythonOperator(task_id="refresh_bi", python_callable=refresh)
        extract_task >> validate_task >> transform_task >> load_task >> refresh_task
