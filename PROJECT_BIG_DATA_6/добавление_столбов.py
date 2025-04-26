
import psycopg2
from config import user,password,host,port,database
from psycopg2 import Error
try:
    # Подключиться к существующей базе данных
    connection = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database)
    connection.autocommit = True
    # Создайте курсор для выполнения операций с базой данных
    # cursor = connection.cursor() ЛИБО ЭТА СТРОКА ИЛИ WITH для работы с запросом 
    
    create_table_query = '''
    CREATE TABLE movies (
    id serial PRIMARY KEY,
    name varchar(100) NOT NULL,
    year int NOT NULL,
    rank float
    );

    CREATE TABLE actors (
    id serial PRIMARY KEY,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    gender char(1)
    );

    CREATE TABLE directors (
    id int PRIMARY KEY, 
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL
    );


    CREATE TABLE directors_genres (
    director_id int REFERENCES directors(id),
    genre varchar(50),
    prob float
    );
                                    

    CREATE TABLE movies_directors (
    director_id int REFERENCES directors(id),
    movie_id int REFERENCES movies(id)
    );

    CREATE TABLE movies_genres (
    movie_id int REFERENCES movies(id),
    genre varchar(50)
    );

    CREATE TABLE roles (
    actor_id int REFERENCES actors(id),
    movie_id int REFERENCES movies(id),
    rolex varchar(50)
    );
    '''
    # Выполнение команды: это создает новую таблицу
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
    
    
    
    # cursor.execute(create_table_query)
    # connection.commit() # установли авто сохранение

except (Exception, Error) as error:
    print("Error when working with PostgreSQL", error)
finally:
    if connection:
        # cursor.close() # либо with 
        connection.close()
        print("Connection to PostgreSQL is closed")


