
import pandas
import psycopg2
from config import user,password,host,port,database
from sqlalchemy import create_engine
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
            filename = file_path
            df = pandas.read_csv(filename)
            engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
            df.to_sql(table_name, engine, if_exists="append", index=False)
            print(f"Data from '{file_path}' imported successfully to '{table_name}' table.")  

except (Exception, Error) as error:
    print("Error when working with PostgreSQL", error)
finally:
    if connection:
        connection.close()
        print("Connection to PostgreSQL is closed")
        