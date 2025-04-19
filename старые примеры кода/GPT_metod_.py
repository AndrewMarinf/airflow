
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
    dag_id='GPT',
    default_args=default_args,
    description='This is our a commend',
    start_date=datetime(2024,2,25,2),
    schedule_interval='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo hello kek'
    )

    task2 = BashOperator(
        task_id='second_task',
        bash_command='echo hey, I am task2 and will be running agter task1!'
    )

    task3 = BashOperator(
        task_id='tried_task',
        bash_command='echo hey, I am task3 and will be running agter task2!'
    )

    #task1.set_downstream(task2)
    #task2.set_downstream(task3)
    task1 >> [task2, task3]
     
    