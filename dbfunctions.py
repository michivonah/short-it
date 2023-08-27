from dotenv import load_dotenv
import os
import psycopg2
import pandas as pd

# load enviromental variables
load_dotenv()

# Create a connection to database
def connectDatabase():
    conn = psycopg2.connect(
        host=os.getenv('DBHOST'),
        database=os.getenv('DBNAME'),
        user=os.getenv('DBUSER'),
        password=os.getenv('DBPASSWORD'),
        port=os.getenv('DBPORT'),)
    conn.autocommit = True
    cursor = conn.cursor()
    return cursor

def executeQuery(query):
    conn = connectDatabase()
    conn.execute(query)
    result = conn.fetchall()
    return result

def executeWithoutFetch(query):
    conn = connectDatabase()
    conn.execute(query)
    return None

def loadTable(query):
    conn = connectDatabase()
    conn.execute(query)
    result = conn.fetchall()
    colnames = [desc[0] for desc in conn.description]
    df = pd.DataFrame(result, columns=colnames)
    return df