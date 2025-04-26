from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 1),
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

dag = DAG(
    'version_2',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)

def test_postgres_connection(**kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='airflow_db')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    result = cursor.fetchone()
    print(f"PostgreSQL version: {result[0]}")
    conn.close()

test_connection_task = PythonOperator(
    # task_id='test_postgres_connection',  было
    task_id='aaa',
    python_callable=test_postgres_connection,
    dag=dag
)

test_connection_task