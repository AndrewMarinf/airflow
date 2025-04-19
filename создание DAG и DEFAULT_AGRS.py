
"""1"""
# Самый простой вариант. Создание переменной класса DAG. 
# В данном случае каждому таску надо обязательно привязываться к DAG'у. 
# И внутри каждого таска явно указывать на DAG.
dag = DAG("dina_simple_dag_v2",
          schedule_interval='@daily',
          default_args=DEFAULT_ARGS,
          max_active_runs=1,
          tags=['karpov']
          )
wait_until_6am = TimeDeltaSensor(
    task_id='wait_until_6am',
    delta=timedelta(seconds=6 * 60 * 60),
    dag=dag                                 # вот это в каждой таскек надо ставить
)

"""2"""
# Он аналогичен первому варианту, но производится через контекстный менеджер. 
# Здесь DAG не нужно указывать внутри каждого таска, он назначается им автоматически.
with DAG(
    dag_id='dina_simple_dag',
    schedule_interval='@daily',
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=['karpov']
) as dag:

    wait_until_6am = TimeDeltaSensor(
        task_id='wait_until_6am',
        delta=timedelta(seconds=6 * 60 * 60)
    )

"""3"""
# Этот вариант появился в Airflow2. DAG создается с помощью декоратора @dag. 
# Нам требуется создать функцию со списком тасков внутри и обернуть ее в декоратор. 
# Таким образом мы получаем переменную класса DAG. 
# Эту переменную мы объявляем в глобальной области видимости, с помощью чего Airflow понимает, что внутри скрипта находится DAG.

@dag(
    start_date=days_ago(12),
    dag_id='dina_simple_dag',
    schedule_interval='@daily',
    default_args=DEFAULT_ARGS,
    max_active_runs=1,
    tags=['karpov']
)
def generate_dag():
    wait_until_6am = TimeDeltaSensor(
        task_id='wait_until_6am',
        delta=timedelta(seconds=6 * 60 * 60)
    )
dag = generate_dag()

"""АРГУМЕНТЫ DAG"""
# Аргументы для DAG передаются в виде словаря при создании. 
# Он нужен для того, чтобы не только какой-то конкретный DAG знал о своем поведении, 
# но и все таски унаследовали это поведение, когда создавались под конкретным DAG'ом.

DEFAULT_ARGS = {
    'owner': 'karpov',                              #- отображает владельца DAG'а в интерфейсе.
    'queue': 'karpov_queue',                        # отвечает за очередь, если несколько worker можем направить таски на разные воркеры
    'pool': 'user_pool',                            # пул, в рамках которого исполняется таск.
    'email': ['airflow@example.com'],               #  - нужен для оповещения о падении и запуске таска.
    'email_on_failure': False,                      # флаг для оповещения в случае падения
    'email_on_retry': False,                        #  флаг для оповещения в случае перезапуска
    'depends_on_past': False,                       # Если True, текущая задача будет ждать успешного выполнения предыдущей задачи перед своим запуском. Установлено значение False, что означает отсутствие такой зависимости.
    'wait_for_downstream': False,                   # Если True, задача будет ожидать завершения всех последующих задач перед тем, как считаться выполненной. Здесь установлено False.
    'retries': 3,                                   #  количество перезапусков таска в случае падения
    'retry_delay': timedelta(minutes=5),            #  время между попытками перезапуска.
    'priority_weight': 10,                          # вес приоритета этого таска перед другими.
    'start_date': datetime(2021, 1, 1),             # время первого запуска. Если это не сегодняшний день, то DAG отработает ровно столько раз, сколько прошло времени между указанным start_date и текущей датой.
    'end_date': datetime(2025, 1, 1),               #  дата, после которой инстансы перестанут генерироваться.
    'sla': timedelta(hours=2),                      #   время, до которого мы ожидаем, что таск завершится. Если этого не случится, придет оповещение и в интерфейсе SLA появится запись о том, что этот таск завершился не вовремя
    'execution_timeout': timedelta(seconds=300),    #  максимальное время выполнения таска. Если таск не успеет выполниться за это время, он будет помечен как FAILED.
    'on_failure_callback': some_function,           #  вызов переданной функции в случае падения
    'on_success_callback': some_other_function,     #  вызов переданной функции в случае успешного завершения
    'on_retry_callback': another_function,          # вызов переданной функции в случае перезапуска
    'sla_miss_callback': yet_another_function,      # вызов переданной функции в случае пропущенного SLA
    'trigger_rule':  'all_success'                  # Он отвечает за то, в каком состоянии должны быть предыдущие таски, чтобы таск, который от них зависит, завершился. По умолчанию это значение all_success.
}
"""пример 'trigger_rule':  'all_success'"""
end = DummyOperator(
    task_id='end',
    trigger_rule='one_success'
)

