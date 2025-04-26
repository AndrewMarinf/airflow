import psycopg2
import csv
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
    cursor = connection.cursor()

    all_tables_dict = {
    "actors": f'/PROJECT_BIG_DATA_6/svs/actors.csv',
    "directors": f'/PROJECT_BIG_DATA_6/svs/directors.csv',
    "directors_genres": f'/PROJECT_BIG_DATA_6/svs/directors_genres.csv',
    "movies": f'/PROJECT_BIG_DATA_6/svs/movies.csv',
    "movies_directors": f'/PROJECT_BIG_DATA_6/svs/movies_directors.csv',
    "movies_genres": f'/PROJECT_BIG_DATA_6/svs/movies_genres.csv',
    "roles": f'/PROJECT_BIG_DATA_6/svs/roles.csv'
    }

    for table_name, file_path in all_tables_dict.items():
        with open(file_path, newline='',encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            columns = ', '.join(reader.fieldnames)
            values_template = ', '.join(['%s'] * len(reader.fieldnames))

            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_template})"
            for row in reader:
                data = [None if value == '' else value for value in row.values()]
                cursor.execute(insert_query, data)

    print("Data imported successfully")


except (Exception, Error) as error:
    print("Error when working with PostgreSQL", error)
finally:
    if connection:
        connection.close()
        print("Connection to PostgreSQL is closed")




 