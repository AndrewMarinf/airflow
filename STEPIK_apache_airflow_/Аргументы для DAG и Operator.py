

"""АРГУМЕНТЫ ДЛЯ DAG"""
''' Начнем с кода который отвечает за создание нашего DAG:'''

'''dag_id '''
# Это уникальное имя, оно будет в отражаться в интерфейсе. Не должно повторяться в рамках различных дагов.
dag = DAG(dag_id='dag',   
         default_args={'owner': 'airflow'},
         schedule_interval='@daily',
         start_date=days_ago(1) )


'''default_args '''
# Это набор параметров которые будут применены к каждому Operator, пример использования ниже, 
# в данном случае, если задача упадет,
# мы попробуем перезапустить её 1 раз, выполнится для всех задач внутри DAG.

args = {'retries': 1}

dag = DAG(
    dag_id='my_dag',
    default_args=args, # Передача списка параметров
    schedule_interval=timedelta(days=1),
    start_date= datetime(2023, 1, 1))


'''start_date '''
# С какой даты мы бы хотели запустить наш пайплайн, например нам хочется чтобы он начал работать с 2023-01-01 
# как в задаче выше. Вы можете задать любую дату/время которая была ранее чем текущий день. 
# Вместе с использованием контекста задачи,
# о котором мы поговорим позже это используется для обеспечения идемпотентности наших ETL процессов



'''schedule_interval '''
# Через какие интервалы нужно запускать задачу. Например такой код timedelta(days=1) будет запускать нашу задачу каждый день. 
# Можно использовать уже знакомое вам cron выражение или набор предопределенных макросов, как например @daily



"""АРГУМЕНТЫ ДЛЯ Opetator"""

load_data = PythonOperator(
    task_id='load_data',  # task_id  Также как и в случае с DAG, это имя нашего Task. В рамках 1 DAG должен быть уникальным
    python_callable=load_data,  #Вызываемая функция, должна быть определена до вызова. Это Python функция в которой мы реализуем наш ETL.
    dag=dag,
    op_kwargs={                      # op_kwargs Передаваемые аргументы в исполняемую функцию.
        'tmp_file': '/tmp/file.csv',
        'table_name': 'table'
    }                      
)

''' еще аргументы DAG'''
# on_failure_callback - определяет функцию обратного вызова (callback), которая будет выполнена в случае сбоя выполнения задачи.

# end_date - определяет конечную дату, после которой DAG автоматически перестанет запускаться.

# retry_delay - определяет интервал времени, через который будет происходить повторный запуск задачи после ошибки.

# owner - определяет владельца (автора) DAG, т.е. человека, ответственного за данное поток данных.

# trigger_rule - определяет правило поведения задачи в случае сбоя или пропуска выполнения.

# email_on_failure - определяет, нужно ли отправлять сообщение об ошибке на электронную почту.



'''trigge_rrule что это и функции к нему как запускать задачи после определенных условий '''
# trigge_rrule в Apache Airflow определяет правило для того, чтобы решить, когда задача должна быть запущена или пропущена, основываясь на статусе других задач. Ниже представлены значения triggerrule и их описание:

# all_failed - Запуск задачи только в случае, если все предыдущие задачи завершились ошибкой.

# dummy - Пустая задача, не выполняющая никаких действий. Обычно используется для организации графа выполнения без выполнения фактических действий.

# one_success - Запуск задачи после успешного завершения хотя бы одной из предыдущих задач.

# one_failed - Запуск задачи после неудачного завершения хотя бы одной из предыдущих задач.

# all_done - Запуск задачи только после завершения всех предыдущих задач (успешно или с ошибкой).

# none_failed - Запуск задачи только в случае, если ни одна из предыдущих задач не завершилась ошибкой.

# all_success - Запуск задачи только в случае, если все предыдущие задачи успешно завершились.