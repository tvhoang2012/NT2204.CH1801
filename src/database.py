import mysql.connector
import os

def free_connection(cursor, connection):
    try:
        cursor.close()
        connection.close()
        return True
    except mysql.connector.Error as err:
        return str(err)


def read_env_file(file_path='env'):
    env_vars = {}
    with open(file_path, 'r') as f:
        for line in f:
            key, value = line.strip().split('=')
            env_vars[key.strip()] = value.strip()
    return env_vars

def create_connection(is_write: bool):
    # env_vars = read_env_file()

    # DATABASE_NAME=env_vars['DATABASE_NAME']
    DATABASE_NAME = os.environ.get('DATABASE_NAME')
    REGION_CODE = os.environ.get('REGION_CODE')
    USER = os.environ.get('USER')
    PASSWORD = os.environ.get('PASSWORD')
    if REGION_CODE == 'us-east-1':
        # HOST = env_vars['RDS_ENDPOINT']
        HOST = os.environ.get('RDS_ENDPOINT')
    else:
        if is_write:
            HOST = os.environ.get('RDS_ENDPOINT')
        else:
            HOST = os.environ.get('RDS_READ_REPLICA')
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE_NAME
        )
        return 200, connection

    except mysql.connector.Error as err:
        return 502, str(err)

def create_table(query):
    status, connection = create_connection(1) 
    if status == 200:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
        except mysql.connector.errors.ProgrammingError as err:
            return 502, str(err)
        finally:
            free_connection(cursor, connection)
        return 200, "Create table success"
    else:
        return 502, connection

def insert_record(query):
    status, connection = create_connection(1) 
    if status == 200:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except mysql.connector.errors.ProgrammingError as err:
            return 502, str(err)
        finally:
            free_connection(cursor, connection)
        return 200, "Insert success"
    else:
        return 502, connection

def select_records(query):
    status, connection = create_connection(0)
    if status == 200:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except mysql.connector.errors.ProgrammingError as err:
            return 502, str(err)
        finally: 
            free_connection(cursor, connection)
        return 200, rows
    else:
        return 502, connection

if __name__ == '__main__':
    status, result = select_records("show databases;")
    print (status, result)