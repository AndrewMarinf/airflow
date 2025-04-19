rom airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def multiply_numbers(number1, number2):
    return number1 * number2

def print_result(context, result):
    print(f'The result is: {result}')

dag = DAG('taskflow_example', start_date=datetime(2022, 1, 1), schedule_interval='@daily')

number1 = 10
number2 = 5

multiply_numbers_task = PythonOperator(
    task_id='multiply_numbers_task',
    python_callable=multiply_numbers,
    op_args=[number1, number2],
    dag=dag
)

print_result_task = PythonOperator(
    task_id='print_result_task',
    python_callable=print_result,
    op_args=[number1, number2],
    provide_context=True,
    dag=dag
)

multiply_numbers_task >> print_result_task