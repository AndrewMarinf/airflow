from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'create_12_23',
    default_args=default_args,
    description='AAAAAs',
    schedule_interval=None,  
)

create_table_sql = """
CREATE TABLE t5(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    value INT NOT NULL
);
"""

create_table = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='aaa',  # Измените на идентификатор вашего подключения
    sql=create_table_sql,
    dag=dag,
)

create_table
