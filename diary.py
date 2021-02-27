import sqlite3

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
            owner TEXT
            destination TEXT,
            description TEXT,
            start_date DATE,
            end_date DATE
        )
    ''')

def insert_diary_record(conn, owner,destination,descritption,start_date,end_date):
    """
    Inserts diary record to the databaze table diary_records.
    Parametr destination must be filled in.
    """
    if not destination:
        return
    c=conn.cursor()
    c.execute(
        "INSERT INTO diary_records (owner,destination, description,start_date,end_date) VALUES (?,?,?)",
        (owner,destination,description,start_date,end_date))
    conn.commit()

def list_diary_records_all(conn):
    """
    returns all diary_records in the databaze
    return value is a list of dicts.
    """
    c=conn.cursor()
    c.execute('''
        SELECT * FROM DESTINATIONS
    ''')
    diary_records = []
    for row in c:
        diary_records.append({
            "id":row[0],
            "owner":row[1],
            "destination":row[2],
            "start_date":row[3],
            "end_date":row[4]
        })
    return diary_records

