TaskFlow API в Apache Airflow - это высокоуровневый API, который предоставляет более удобный и интуитивно понятный способ определения и управления задачами в ваших пайплайнах. Этот API предоставляет набор классов и методов, которые упрощают создание и организацию задач, а также управление их выполнением и зависимостями.

# Принцип работы TaskFlow API в Airflow:

# 1. Создание задач:
#    - Вместо использования Operator'ов для определения задач, вы можете создавать объекты классов Task и BaseOperator, которые предоставляются TaskFlow API.
   
# 2. Определение зависимостей:
#    - TaskFlow API позволяет явно определять зависимости между задачами с помощью методов set_downstream() и set_upstream(), что делает управление выполнением задач более удобным.
   
# 3. Управление выполнением задач:
#    - TaskFlow API предоставляет более гибкий способ управления выполнением задач, например, путем установки правил выполнения и обработки исключений.
   
# Пример использования TaskFlow API:


from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator

dag = DAG('taskflow_example', start_date=days_ago(1), schedule_interval='@daily')

# Определение задач с использованием TaskFlow API
start_task = DummyOperator(task_id='start', dag=dag)
end_task = DummyOperator(task_id='end', dag=dag)

def print_hello():
    return 'Hello, Airflow!'

task1 = PythonOperator(task_id='print_hello', python_callable=print_hello, dag=dag)

# Устанавливаем зависимости между задачами
start_task >> task1 >> end_task

# или так:
# task1.set_upstream(start_task)
# end_task.set_upstream(task1)


# В этом примере мы создаем три задачи: start_task, task1 (которая вызывает функцию print_hello) и end_task,
# и устанавливаем зависимости между ними с использованием TaskFlow API. 
# Затем мы добавляем эти задачи в даг и задаем их порядок выполнения.

# Таким образом, TaskFlow API в Apache Airflow предоставляет более удобный и гибкий способ определения и
# управления задачами в ваших пайплайнах, что делает разработку и поддержку ваших рабочих процессов более простой и 
# эффективной