
from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'coder2j',    # кто владелец 
    'retries': 4,          # число попыток
    'retry_delay': timedelta(minutes=2) # время ожидания для каждой повторной попытки 
}
with DAG( 
    dag_id = 'my_test_dag_1_and_dag_5',
    default_args = default_args, # установили настройки по умолчанию
    description = 'This is our a commend',
    start_date = datetime(2024,2,25,2),
    schedule_interval = '@daily'
) as dag:
    task1 = BashOperator(
        task_id = 'first_task',
        bash_command = 'hello kek'
    )

    task2 = BashOperator(
        task_id = 'second_task',
        bash_command = 'echo hey, I am task2 and will be running agter task2! '
    )

    task3 = BashOperator(
        task_id = 'tried_task',
        bash_command = 'echo hey, I am task2 and will be running agter task3!'
    )
    #task1.set_downstream(task2)
    #task1.set_downstream(task3) 
    task1 >> [task2, task3] 
    #task1 >> task2
    #task1 >> task3