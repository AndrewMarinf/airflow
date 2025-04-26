
''' Документация'''
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

def f_callable():
  print("Hello World!")

dag = DAG('dag',schedule_interval=timedelta(days=1), start_date=days_ago(1))
# Создадим оператор для исполнения python функции
t1 = PythonOperator(task_id='print', python_callable=f_callable,dag=dag)

# Документация
t1.doc_md = "Task Documentations :)"
dag.doc_md = "Dag Documentations :)"



'''Зависимости'''
# 1 пример
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
 
# Создадим объект класса DAG
dag =  DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1))

# Создадим несколько шагов, которые будут параллельно исполнять dummy(пустые)команды
t1 = DummyOperator(task_id='task_1', dag=dag)
t2 = DummyOperator(task_id='task_2', dag=dag)
t3 = DummyOperator(task_id='task_3', dag=dag)
t4 = DummyOperator(task_id='task_4', dag=dag)

# Настройка зависимостей
t1 >> [t2, t3] >> t4
t1 >> [t2, t3]  #Исполнение t2, t3 будет только после t1

# 2 пример  #херня короче 

from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
 
dag = DAG('dag',schedule_interval=timedelta(days=1), start_date=days_ago(1))
t1 = DummyOperator(task_id='task_1', dag=dag)
t2 = DummyOperator(task_id='task_2',dag=dag)
t3 = DummyOperator(task_id='task_3',dag=dag)
t4 = DummyOperator(task_id='task_4',dag=dag)


t1.doc_md = "Task Documentations :)"
dag.doc_md = __doc__ 
dag.doc_md = "Dag Documentations :)"
 
t1 >> t2 >> [t3, t4]


