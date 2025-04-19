
import pendulum
import requests
from airflow.decorators import task, dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airlow .providers.postgres.hooks.postgres import PostgresHook
import os, tempfile

os.environ['NO_PROXY'] = '*'

sql_schema_init = """
CREATE TABLE IF NOT EXISTS public.type_marijuana AS( 
    # name varchar NULL,
    # price int NULL
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

CREATE MATERIALIZED VIEW IF NOT EXISTS piblic.type_marijuana_itog AS(
    SELECT * FROM public.products 
);
"""
sql_refresh_view = """
REFRESH MATERIALIZED VIEW pulic.type_marijuana_itog
"""

@dag(
    'dag_api',
    schedule_interval = '0 */12 * * *',
    tags = ['api'],
    start_dat = pendulum.datetime(2024, 8, 30),
    catchup = False,
    default_args = {
        'owner: 'andrew'
    }
)
def dag_api():
    schema_init = PostgresOperator(
        task_id = 'schema_init',             # имя нашей таски 
        postgres_conn_id = 'test_db',
        sql = sql_schema_init
    )
    refresh = PostgresOperator(
        task_id = 'refresh',                # имя нашей таски
        postgres_conn_id = 'test_db',
        sql = sql_refresh_view
    )
    @task
    def transfer_date_api(**context):
#        date = context['dag_run'].date_interval_start.date()
        url = 'https://random-data-api.com/api/cannabis/random_cannabis?size=10' # + date.starftime("%Y%m%d")
        response = requests.get(url)
        response.encoding = 'utf-8'
        r = response.json()
        out = ''
        str = ''
        for i in r:
            str = f"{i['name']}\t{['price']}\n"
            out += str


        with tempfile.NamedTemporaryFile(mode='w', delete=False) as _tmp:
            _tmp.write(out)
            tmp_file = _tmp.name
        try:
            hook = PostgresHook(postgres_conn_id = 'test_db')
            hook.bulk_load('type_marijuana', tmp_file)
        finally:
            os.remove(tmp_file)

    schema_init >> transfer_date_api() >> refresh

mydag = dag_api()
