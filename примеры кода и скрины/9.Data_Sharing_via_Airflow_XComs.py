# Airflow XComs (или Cross-communication) - это способ обмена данных между задачами в пайплайне Airflow. 
# Они позволяют передавать информацию от одной задачи к другой, что очень удобно при работе с большим количеством задач, 
# требующих обмена данными.

# Принцип работы XComs довольно прост: задача A может передавать данные задаче B через XCom, 
# а задача B может использовать эти данные для своего выполнения. 
# Данные могут быть любым типом (строки, числа, словари и т. д.),
# и их можно передать как результат выполнения задачи, так и явно задав в коде.

# Пример использования XComs:

# 1. Допустим, у нас есть две задачи: task1 и task2. Мы хотим передать результат выполнения task1 в task2.


from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

def extract_data():
    return {'key': 'value'}

def process_data(**kwargs):
    data = kwargs['task_instance'].xcom_pull(task_ids='task1')
    print(data)

dag = DAG('data_pipeline', description='Data pipeline with XComs', schedule_interval='0 0 * * *', start_date=datetime.datetime(2022, 1, 1), catchup=False)

task1 = PythonOperator(task_id='task1', python_callable=extract_data, dag=dag)

task2 = PythonOperator(task_id='task2', python_callable=process_data, dag=dag)

task1 >> task2


# 2. В этом примере task1 возвращает словарь {'key': 'value'}. Затем task2 использует xcom_pull метод, 
# чтобы получить этот словарь из task1 и вывести его на консоль.

# 3. При выполнении дага Airflow автоматически передаст данные от task1 к task2 через XCom.

# Итак, XComs - это мощный механизм обмена данными между задачами в Airflow, 
# который позволяет создавать более сложные пайплайны обработки данных. 
# Они делают взаимодействие между задачами более гибким и эффективным, 
# и позволяют передавать любые данные между задачами в вашем пайплайне.