import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    '''create connection to slqite database
    param
       db_file - path to sqlite database
    return
        conn - connection object or None
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def create_table():
    """
    """
    pass


def init_database(db_file):
    """Initialize db and create seedlings and availability_dates table
    param
       db_file - path to sqlite database
    return
        None
    """
    # Create seedlings table
    create_seedlings_table = """
    CREATE TABLE IF NOT EXISTS seedlings(
        plant_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        price text,
        img_url TEXT
    );"""

    # Create availability_dates table
    create_availability_date = """
    CREATE TABLE IF NOT EXISTS availability_dates(
        plant_id INTEGER NOT NULL,
        available_date TEXT NOT NULL,
        FOREIGN KEY (plant_id) REFERENCES seedlings (plant_id)
    );"""

    pass
