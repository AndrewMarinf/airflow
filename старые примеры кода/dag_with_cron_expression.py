
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


# настройки по умолчанию
default_args = {
    'owner': 'coder2j',
    'retries': 4,
    'retry_delay': timedelta(minutes=5)
}
with DAG( 
    dag_id='dag_with_cron_expression_v03',
    default_args=default_args,
    description='This is our a commend',
    start_date=datetime(2024,2,20,2),
    #schedule_interval='@daily' # тут с какой переодичностью запускается 1 варик
    schedule_interval = '0 3 * * Tue,Fri' # тут 2 вариант  # https://crontab.guru/ тут можно проверить
    #schedule_interval = '0 3 * * Tue-Fri' с вторника по пятницу 
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo hello kek'
    )
    task1