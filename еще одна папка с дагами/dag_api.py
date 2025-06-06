import pendulum
import requests
from airflow.decorators import task, dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import os
import tempfile


# SQL для создания таблицы и представления
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

CREATE MATERIALIZED VIEW IF NOT EXISTS public.type_marijuana_itog AS (
    SELECT * FROM public.type_marijuana
);
"""

# SQL для обновления материализованного представления
sql_refresh_view = """
REFRESH MATERIALIZED VIEW public.type_marijuana_itog;
"""

@dag(
    'dag_api',
    schedule_interval='0 */12 * * *',
    tags=['api'],
    start_date=pendulum.datetime(2024, 8, 30),
    catchup=False,
    default_args={
        'owner': 'andrew'
    }
)
def dag_api():
    # Операция создания схемы и представления
    schema_init = PostgresOperator(
        task_id='schema_init',
        postgres_conn_id='api_db',
        sql=sql_schema_init
    )

    # Операция обновления материализованного представления
    refresh = PostgresOperator(
        task_id='refresh',
        postgres_conn_id='api_db',
        sql=sql_refresh_view
    )

    @task
    def transfer_data_api(**context):
        url = 'https://random-data-api.com/api/cannabis/random_cannabis?size=10'
        response = requests.get(url)
        response.encoding = 'utf-8'
        records = response.json()

        # Формирование данных для вставки в таблицу
        out = ''
        for record in records:
            line = f"{record['id']}\t{record['uid']}\t{record['strain']}\t{record['cannabinoid_abbreviation']}\t{record['cannabinoid']}\t"
            line += f"{record['terpene']}\t{record['medical_use']}\t{record['health_benefit']}\t{record['category']}\t"
            line += f"{record['type']}\t{record['buzzword']}\t{record['brand']}\n"
            out += line

        # Запись данных во временный файл
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as _tmp:
            _tmp.write(out)
            tmp_file = _tmp.name

        # Загрузка данных в PostgreSQL
        try:
            hook = PostgresHook(postgres_conn_id='api_db')
            hook.bulk_load('type_marijuana', tmp_file)
        finally:
            os.remove(tmp_file)

    # Определение порядка выполнения задач
    schema_init >> transfer_data_api() >> refresh

# Создание DAG
mydag = dag_api()
