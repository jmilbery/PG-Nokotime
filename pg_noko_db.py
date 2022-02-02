#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Creates/updates PostgreSQL database
# ---------------------------------------------------------------------------

import psycopg2
import sys
import pg_noko_logger
import config


conn = psycopg2.connect(dbname=config.dbname, user=config.user, 
    password=config.password,host=config.host, port=config.port)


def test_db_connection():
    """ Test connection to the PosgreSQL database (test out settings in INI before drop/create)"""
    try:
        cur = conn.cursor()
        cur.execute("""SELECT user""")
        rows = cur.fetchall()
        for row in rows:
            print ("   ", row[0])
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E","Test_db_connection",str(error))
        sys.exit("ERROR -- Execute_sql failed")

def execute_sql(sql_statement, data):
    try:
        cur = conn.cursor()
        cur.execute(sql_statement,data)
        conn.commit()
        pg_noko_logger.log("I","EXECUTE_SQL",sql_statement)
        pg_noko_logger.log("I","EXECUTE_SQL",data)
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E","EXECUTE_SQL",str(error))
        sys.exit("ERROR -- Execute_sql failed")


def execute_ddl(sql_statement):
    try:
        cur = conn.cursor()
        cur.execute(sql_statement)
        conn.commit()
        pg_noko_logger.log("I","EXECUTE_DDL",sql_statement)
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E","EXECUTE_DDL",str(error))
        sys.exit("ERROR -- Execute_ddl failed")
 


