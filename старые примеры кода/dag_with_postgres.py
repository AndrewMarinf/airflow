


"""так и не удалось это сделать"""
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}
with DAG( 
    dag_id='dag_wint_postgres_operator_v02',
    default_args=default_args,
    description='This is our a commend',
    start_date=datetime(2024,2,27,2),
    schedule_interval = '0 0 * * *',
    #schedule_interval='@daily'
) as dag:
    task1 = PostgresOperator(
        task_id = 'create_postgres_table',
        postgres_conn_id = 'postgres_localhost',
        sql = """
            create table if not exists dag_runs(
            dt date,
            dag_id character varying,
            primary key (dt,dag_id)
            )"""
    )

    task2 = PostgresOperator(
        task_id = 'insert_into_table',
        postgres_conn_id = 'postgres_localhost',
        sql = """
                insert into dag_runs(dt, dag_id) values ( '{{ds}}','{{dag.dag_id}}')
                """
    )
    task1 >> task2

    