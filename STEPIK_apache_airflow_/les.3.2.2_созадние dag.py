""" Как создать DAG""" 

# Первым делом мы импортируем необходимый class
# После чего создаем объект DAG Какие аргументы принимает DAG мы разберем в следующем шаге.

dag =  DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1)) # это просто как выглядит

# Есть два основных способа создать DAG, первый "простой" второй с помощью контекстного менеджера, при помощи with

""" 1 вариант"""
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
 
# Создадим объект класса DAG
dag =  DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1))

"""2 вариант"""
from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
 
# Создадим объект класса DAG
with DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1)) as dag:
  pass