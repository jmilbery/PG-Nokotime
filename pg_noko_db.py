#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Creates/updates PostgreSQL database
# ---------------------------------------------------------------------------
import psycopg2
import pg_noko_logger
from configparser import ConfigParser


""" Read the pg_noko.ini configuration file to get NOKO API parameters and PostgreSQL DB parameters"""


try:
    configur = ConfigParser()
    configur.read('pg_noko.ini')
    ini_dbname = configur.get('db','dbname')
    ini_user = configur.get('db','user')
    ini_password = configur.get('db','password')
    ini_host = configur.get('db','host')
    ini_port = configur.get('db','port')
    ini_schema = configur.get('db','schema')
except:
    pg_noko_logger.log("Missing PostgreSQL INI Settings")
    quit()

pg_noko_logger.log("I",'database: '+ini_dbname)
pg_noko_logger.log("I",'user: '+ini_user)
pg_noko_logger.log("I",'pwd: '+ini_password)
pg_noko_logger.log("I",'host: '+ini_host)
pg_noko_logger.log("I",'host: '+ini_port)
pg_noko_logger.log("I",'schema: '+ini_schema)

conn = psycopg2.connect(dbname=ini_dbname, user=ini_user, password=ini_password,host=ini_host, port=ini_port)

def test_db_connection():
    cur = conn.cursor()
    cur.execute("""SELECT user""")
    rows = cur.fetchall()
    for row in rows:
        print ("   ", row[0])
    cur.close()
    conn.close()

def drop_tables():
    sql_drop_noko_raw_entries = "drop table if exists "+ ini_schema+ ".noko_raw_entries cascade"
    try:
        conn = psycopg2.connect(dbname=ini_dbname, user=ini_user, password=ini_password,host=ini_host, port=ini_port)
        cur = conn.cursor()
        cur.execute(sql_drop_noko_raw_entries)
        conn.commit()
        pg_noko_logger.log("I",sql_drop_noko_raw_entries)
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E",str(error))
    finally:
        cur.close()
        conn.close()

def create_tables():
    sql_create_noko_raw_entries = """CREATE TABLE postgres.noko.noko_raw_entries (
	noko_entry_id bigint NOT NULL,
	noko_user varchar(512),
	noko_date date,
	noko_minutes integer,
	noko_desc varchar(2048),
	load_date date,
	PRIMARY KEY (noko_entry_id)
    );
    """
    print (sql_create_noko_raw_entries)
