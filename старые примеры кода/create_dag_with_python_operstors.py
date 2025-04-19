
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

def greet(age,ti) -> str:
    #name = ti.xcom_pull(task_ids='get_name')    было так
    first_name = ti.xcom_pull(task_ids='get_name',key='first_name')
    last_name = ti.xcom_pull(task_ids = 'get_name', key='last_name')
    age = ti.xcom_pull(task_ids = 'get_age', key = 'age')
    print(f'Hello Word! My name is {first_name},{last_name}'
    #print(f'Hello Word! My name is {name},'
          f'and I am {age} years old!)')

def get_name(ti) -> str:
   ti.xcom_puch(key = 'first_name',value ='Jerry')
   ti.xcom_puch(key = 'last_name',value = 'Fridman')

def get_age(ti):
    ti.xcom_push(key= 'age', value = 19)   

with DAG(
    dag_id='our_dag_wint_python_operator_v06',
    default_args=default_args,
    description='This is our a commend',
    start_date=datetime(2024,2,25,2),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id = 'greet',
        python_callable = greet,
       # op_kwargs={ 'age': 40}   # тут запихнули параметры в функцию
    )

    task2 = PythonOperator(
        task_id = 'get_name',
        python_callable = get_name
    )

    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable = get_age
    )
    [task2,task3] >> task1 

