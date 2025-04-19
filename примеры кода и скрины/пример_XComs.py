
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def multiply_numbers(**context):
    number1 = context['task_instance'].xcom_pull(task_ids='set_number1')
    number2 = context['task_instance'].xcom_pull(task_ids='set_number2')
    result = number1 * number2
    context['task_instance'].xcom_push(key='result', value=result)

def print_result(**context):
    result = context['task_instance'].xcom_pull(key='result', task_ids='multiply_numbers')
    print(f'The result is: {result}')

dag = DAG('xcom_example', start_date=datetime(2022, 1, 1), schedule_interval='@daily')

set_number1 = PythonOperator(
    task_id='set_number1',
    python_callable=lambda: 10,
    dag=dag
)

set_number2 = PythonOperator(
    task_id='set_number2',
    python_callable=lambda: 5,
    dag=dag
)

multiply_numbers = PythonOperator(
    task_id='multiply_numbers',
    python_callable=multiply_numbers,
    dag=dag
)

print_result = PythonOperator(
    task_id='print_result',
    python_callable=print_result,
    dag=dag
)

set_number1 >> set_number2 >> multiply_numbers >> print_result
