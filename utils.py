import random
import mariadb
import sys

def random_hex():
    return '{:02x}'.format(random.randint(0, 255))

def generate_hex(count):
    str_hex="FE"
    for i in range(count-2):
        str_hex+=random_hex()
    return str_hex+"FF"

def connect_db():
    try:
        conn = mariadb.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            db="joaelec"
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def execute_query(conn,query,data):
    cursor = conn.cursor()
    cursor.execute(query,data)
    conn.commit()
