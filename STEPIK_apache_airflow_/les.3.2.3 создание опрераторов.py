
'''DummyOperator'''

# Начнем с самого простого он просто ничего не делает. Отрабатывает и передает управление дальше.

from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
 
# Создадим объект класса DAG
dag =  DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1))

# Создадим dummy(пустые)команду
t1 = DummyOperator(task_id='task_1', dag=dag)


'''BashOperator'''

from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator

# Создадим объект класса DAG
dag =  DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1))

# Создадим несколько шагов, которые будут параллельно исполнять dummy(пустые)команды
t1 = BashOperator(task_id='task_1',
                  bash_command='cat /root/airflow/dags/dag.py',
                  dag=dag)




'''PythonOperator'''

# Самый часто используемый на практике, он служит для запуска любого python кода который вы напишите в вашей функции.
#  Используется интерпретатор по умолчанию (однако есть специальный оператор PythonVirtualenvOperator, 
# который создает локальное окружение для конкретной задачи и запускает код там)

# Данный код запустит функцию print_context

from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

# Создадим объект класса DAG
dag =  DAG('dag', schedule_interval=timedelta(days=1), start_date=days_ago(1))

def print_context():
    return 'Hello World'

run_this = PythonOperator(
    task_id='print_the_context',
    python_callable=print_context,
    dag=dag,
)

# EmailOperator                   Отправит письмо на почту
# BaseOperator                    Базовый класс для всех операторов
# BaseBranchOperator              Базовый класс для создания разветвлений
# ShortCircuitOperator            Если вернет False то последующие таски будут пропущены
# PythonVirtualenvOperator        Выполняет Python код в изолированном окружении
# DockerOperator                  Выполнит команду внутри контейнера





