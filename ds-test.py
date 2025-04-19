
"""
Тестовый даг
"""
# Импорт необходимых модулей Airflow
from airflow import DAG
from airflow.utils.dates import days_ago
import logging

# Импорт операторов Airflow для различных типов задач
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator

# Определение аргументов по умолчанию для DAG
DEFAULT_ARGS = {
    'start_date': days_ago(2),  # Указывает дату начала выполнения DAG
    'owner': 'd-s',  # Владелец DAG
    'poke_interval': 600  # Интервал проверки состояния задачи (в секундах)
}

# Создание экземпляра DAG с указанием его параметров и аргументов по умолчанию
with DAG("ds_test"
         , schedule_interval='@daily'  # Запуск DAG ежедневно
         , default_args=DEFAULT_ARGS
         , max_active_runs=1  # Максимальное количество одновременно активных запусков DAG
         , tags=['d-s']  # Теги для удобства фильтрации DAG в интерфейсе Airflow
         ) as dag:

    # Создание задачи DummyOperator, которая ничего не делает и служит для тестирования или контроля потока выполнения
    dummy = DummyOperator(task_id="dummy")

    # Создание задачи BashOperator, которая выполняет bash команду. В данном случае команда выводит значение переменной ds (дата запуска)
    echo_ds = BashOperator(
        task_id='echo_ds',
        bash_command='echo {{ ds }}',  # Команда для выполнения
        dag=dag  # Привязка оператора к текущему DAG
    )

    # Определение функции Python, которая будет вызвана PythonOperator
    def hello_world_func():
        logging.info("Hello World!")  # Вывод сообщения в лог

    # Создание задачи PythonOperator, которая выполняет указанную функцию Python
    hello_world = PythonOperator(
        task_id='hello_world',  # Идентификатор задачи
        python_callable=hello_world_func,  # Функция для выполнения
        dag=dag  # Привязка оператора к текущему DAG
    )

    # Определение последовательности выполнения задач: сначала выполняется dummy, затем параллельно echo_ds и hello_world
    dummy >> [echo_ds, hello_world]


