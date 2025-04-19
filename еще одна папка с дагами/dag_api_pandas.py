import pendulum
import requests
import pandas as pd
from airflow.decorators import task, dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

# SQL для создания таблицы
sql_schema_init = """
CREATE TABLE IF NOT EXISTS public.type_marijuana (
    id SERIAL PRIMARY KEY,
    uid TEXT,
    strain TEXT,
    cannabinoid_abbreviation TEXT,
    cannabinoid TEXT,
    terpene TEXT,
    medical_use TEXT,
    health_benefit TEXT,
    category TEXT,
    type TEXT,
    buzzword TEXT,
    brand TEXT
);
"""

@dag(
    'dag_api_pandas',
    schedule_interval='0 */12 * * *',
    tags=['api'],
    start_date=pendulum.datetime(2024, 8, 30),
    catchup=False,
    default_args={
        'owner': 'andrew'
    }
)
def dag_api():
    # Операция создания схемы
    schema_init = PostgresOperator(
        task_id='schema_init',
        postgres_conn_id='api_db',
        sql=sql_schema_init
    )

    @task
    def transfer_data_api(**context):
        url = 'https://random-data-api.com/api/cannabis/random_cannabis?size=10'
        response = requests.get(url)
        response.encoding = 'utf-8'
        records = response.json()

        # Преобразование данных в DataFrame
        df = pd.DataFrame(records)

        # Подключение к базе данных и загрузка данных
        hook = PostgresHook(postgres_conn_id='api_db')
        engine = hook.get_sqlalchemy_engine()

        # Запись данных в таблицу
        df.to_sql('type_marijuana', engine, if_exists='append', index=False)

    # Определение порядка выполнения задач
    schema_init >> transfer_data_api()

# Создание DAG
mydag = dag_api()
