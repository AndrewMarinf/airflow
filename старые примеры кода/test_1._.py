from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'coder2j',
    'retries': 4,
    'retry_delay': timedelta(minutes=2)
}
with DAG( 
    dag_id='TEST_1',
    default_args=default_args,
    description='This is our a commend',
    start_date=datetime(2024,2,25,2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='FIRST_TASK_111',
        bash_command='echo hello kek'
    )
    task1