from datetime import date
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


def create_table(conn, sql_cmd):
    """Create table from `sql_cmd`
    Args
        conn: database connection
        sql_cmd (str): SQL statement to be executed
    """
    c = conn.cursor()
    c.execute(sql_cmd)


def init_database(conn, db_file):
    """Initialize db and create seedlings and availability_dates table
    Args
        conn: database connection
       db_file (Path)- path to sqlite database
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
    # Create tables
    create_table(conn, create_seedlings_table)
    create_table(conn, create_availability_date)


def id_names_from_db(conn):
    """Return a dictionary of plant_id and name from db.

    Args
        conn: database connection
    Returns:
        id_name_dict (dict): dictionary of plant_id and name
    """
    c = conn.cursor()
    c.execute("SELECT plant_id, name FROM seedlings")
    rows = c.fetchall()
    id_name_dict = dict(rows)
    return id_name_dict


def update_availability_dates_table(conn, new_plant_index):
    """Insert latest seedlings available with todays date into db.
    Args
        conn: database connection
        new_plant_index (list): list of tuples (plant_id, name)
    """
    todays_date = date.today()
    # get data in correct tuple format (plant_id, date) for insert into db
    plant_id_date = list(((d, str(todays_date)) for d in new_plant_index))

    c = conn.cursor()
    c.executemany("INSERT INTO availability_dates (plant_id, available_date) \
                        VALUES (?, ?)",
                        plant_id_date)


def update_seedlings_table(conn, name_li, descr_li, sale_price, pic_li):
    """Insert new seedling data into db.seedlings table
    Args
        conn: database connection
        name_li (list):
        descr_li (list):
        sale_price (list):
        pic_li (list):

    """
    c = conn.cursor()
    for i in range(len(name_li)):
        c.execute("INSERT INTO seedlings (name, description, price, img_url) \
                  VALUES (?, ?, ?, ?)",
                  (name_li[i], descr_li[i], sale_price[i], pic_li[i]))
