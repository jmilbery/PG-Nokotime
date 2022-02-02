#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Creates/updates PostgreSQL database
# ---------------------------------------------------------------------------

import psycopg2
import sys
import pg_noko_logger
from configparser import ConfigParser


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
    pg_noko_logger.log("E","Missing PostgreSQL INI Settings")
    quit()

pg_noko_logger.log("I",'database: '+ini_dbname)
pg_noko_logger.log("I",'user: '+ini_user)
pg_noko_logger.log("I",'pwd: '+ini_password)
pg_noko_logger.log("I",'host: '+ini_host)
pg_noko_logger.log("I",'host: '+ini_port)
pg_noko_logger.log("I",'schema: '+ini_schema)

conn = psycopg2.connect(dbname=ini_dbname, user=ini_user, password=ini_password,host=ini_host, port=ini_port)


def test_db_connection():
    """ Test connection to the PosgreSQL database (test out settings in INI before drop/create)"""
    cur = conn.cursor()
    cur.execute("""SELECT user""")
    rows = cur.fetchall()
    for row in rows:
        print ("   ", row[0])
    cur.close()
    conn.close()

def execute_sql(sql_statement, data):
    try:
        conn = psycopg2.connect(dbname=ini_dbname, user=ini_user, password=ini_password,host=ini_host, port=ini_port)
        cur = conn.cursor()
        cur.execute(sql_statement,data)
        conn.commit()
        pg_noko_logger.log("I",sql_statement)
        pg_noko_logger.log("I",data)
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E",str(error))
        sys.exit("ERROR -- Execute_sql failed")
    finally:
        cur.close()
        conn.close()


def execute_ddl(sql_statement):
    try:
        conn = psycopg2.connect(dbname=ini_dbname, user=ini_user, password=ini_password,host=ini_host, port=ini_port)
        cur = conn.cursor()
        cur.execute(sql_statement)
        conn.commit()
        pg_noko_logger.log("I",sql_statement)
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E",str(error))
    finally:
        cur.close()
        conn.close()


