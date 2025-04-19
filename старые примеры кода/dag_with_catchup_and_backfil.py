from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import timedelta

default_args = {
    'owner': 'coder2j',
    'retries': 4,
    'retry_delay': timedelta(minutes=2)
}

with DAG( 
    dag_id='catchup_and_backfil_v02',
    default_args=default_args,
    description='This is our a commend',
    start_date=datetime(2024,2,25,2),
    schedule_interval='@daily',
    catchup = True
) as dag:
    task1 = BashOperator(
    task_id='task1',
    bash_command='lol kek'
    )