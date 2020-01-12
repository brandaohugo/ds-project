import sqlite3
import os
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


ROOT_DIR = os.path.dirname(os.path.abspath('ds-project'))  # This is your Project Root
print(ROOT_DIR)