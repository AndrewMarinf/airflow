
from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'coder2j',    # кто владелец 
    'retries': 5,          # число попыток
    'retry_delay': timedelta(minutes=2) # время ожидания для каждой повторной попытки 
}
with DAG( 
    dag_id = 'my_test_dag_2',
    default_args = default_args, # установили настройки по умолчанию
    description = 'This is our a commend',
    start_date = datetime(2021,7,29,2),
    schedule_interval = '@daily'
) as dag:
    # тут пошли таски с операторами
    task1 = BashOperator(
        task_id = 'first_task_2',
        bash_command = 'hello kek'
    )

    task1