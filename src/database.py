import mysql.connector


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

def create_connection():
    env_vars = read_env_file()
    try:
        connection = mysql.connector.connect(
            host=env_vars['RDS_ENDPOINT'],
            user=env_vars['USER'],
            password=env_vars['PASSWORD'],
            database=env_vars['DATABASE_NAME']
        )
        return 200, connection

    except mysql.connector.Error as err:
        return 502, str(err)

def create_table(query):
    status, connection = create_connection() 
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
    status, connection = create_connection() 
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
    status, connection = create_connection()
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