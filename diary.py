import sqlite3
import datetime
from datetime import date

db_path = 'databaze.db'


def get_conn():
    """
    Prepares connection to the databaze
    """
    #Domluvit s anyou jakou databazi
    db_path = 'databaze.db'
    try:
        return sqlite3.connect(db_path)
    except Exception as e:
        raise Exception


def prepare_schema(conn):
    """
    Prepares table for this application,
    if tables already exist nothing happens
    """
    c=conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS diary_records (
            id INTEGER PRIMARY KEY,
            username TEXT,
            country TEXT,
            place TEXT,
            date_from DATE,
            date_to DATE,
            text TEXT
        )
    ''')

def insert_diary_record(username,country,place,date_from,date_to,text):
    """
    Inserts diary record to the databaze table diary_records.
    Parametr destination must be filled in.
    """
    conn = get_conn()
    c=conn.cursor()
    c.execute(
        "INSERT INTO diary_records (username,country,place,date_from,date_to,text) VALUES (?,?,?,?,?,?)",
        (username,country,place,date_from,date_to,text))
    conn.commit()

def list_diary_records_all():
    """
    returns all diary_records in the databaze
    return value is a list of dicts.
    """
    conn = get_conn()
    c=conn.cursor()
    c.execute('''
        SELECT * FROM DIARY_RECORDS
    ''')
    diary_records = []
    for row in c:
        diary_records.append({
            "id":row[0],
            "username":row[1],
            "country":row[2],
            "place":row[3],
            "date_from":row[4],
            "date_to":row[5],
            "text":row[6]
        })
    return diary_records

def list_diary_records_countries(country):
    """
    returns diary_records in the databaze to chosen country
    return value is a list of dicts.
    """
    conn = get_conn()
    c=conn.cursor()
    c.execute('''
        SELECT * FROM DIARY_RECORDS WHERE COUNTRY = ?''',(country,))
    diary_records = []
    for row in c:
        diary_records.append({
            "id":row[0],
            "username":row[1],
            "country":row[2],
            "place":row[3],
            "date_from":row[4],
            "date_to":row[5],
            "text":row[6]
        })
    return diary_records

def list_diary_records_username (username):
    """
    returns all diary records made by logged in owner
    :param conn:
    :param owner:
    :return:
    """
    conn = get_conn()
    c = conn.cursor()

def list_diary_records_random ():
    """
    returns one diary record chosen randomly
    :param conn:
    :param owner:
    :return:
    """
    conn = get_conn()
    c = conn.cursor()
    diary_record = c.execute('''
            SELECT * FROM DIARY_RECORDS ORDER BY RANDOM() LIMIT 1
        ''')
    diary_records = []
    for row in c:
        diary_records.append({
            "id":row[0],
            "username":row[1],
            "country":row[2],
            "place":row[3],
            "date_from":row[4],
            "date_to":row[5],
            "text":row[6]
        })
    return diary_records