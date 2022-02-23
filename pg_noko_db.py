#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Drops/Creates/updates PostgreSQL database tables
# ---------------------------------------------------------------------------
""" Library to connect to the database and execute SQL statements"""
import psycopg2
import sys
import pg_noko_logger
import config
#
# This one is far from perfect.  For very large data sets you might want to
# preserve connections across db calls and you would definitely want to "batch"
# inserts.   Psycopg2 allows you to embed multiple inserts into a single SQL string,
# and you could do that here -- this will greatly reduce DB roundtrips -- we did
# not need to do this given our relatively small data sets < 100k entries.  On the plus
# side, all DB access is isolated to this library.

#
# Create the db connection string from fields in the config.py library
#

def connect_db():
    conn = psycopg2.connect(dbname=config.dbname, user=config.user, 
    password=config.password,host=config.host, port=config.port)
    return conn

def close_db(conn):
    conn.close()

def test_db_connection(conn):
    """ Test connection to the PosgreSQL database (test out settings in INI before drop/create)"""
    #
    # We added this to make it simple to test out the connection to the DB before you
    # try fetching data and entering records.
    #
    # python3 pg_noko_maing.py --test_db_connection
    #
    try:
        conn.cursor().execute("""SELECT user""")
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E","Test_db_connection",str(error))
        sys.exit("ERROR -- Execute_sql failed connectint to the db")

def execute_sql(conn,sql_statement, data):
    """ Execute a DELETE/UPDATE/INSERT SQL statement"""
    #
    # Pass the SQL string in psycopg2 format and the column data
    # as a python list
    #
    try:
        conn.cursor().execute(sql_statement,data)
        conn.commit()
        #
        # Very simple logging, we did not bother with the python logging
        # library which is much more comprehensive.   We pass the SQL
        # statement and the data to the log method.   If config.py has
        # log_message set to true, it will output the data to stdout.
        # We log everything, if you don't want to display it, then set the log_message
        # variable to false in config.py
        #
        pg_noko_logger.log("I","EXECUTE_SQL",sql_statement)
        pg_noko_logger.log("I","EXECUTE_SQL",data)
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Log the error if the SQL fails
        #
        pg_noko_logger.log("E","EXECUTE_SQL",str(error))
        #
        # This is not very resilient, but we did not want to plumb in
        # logic to re-start where we left off.   If any SQL fails, we
        # report the failure and exit -- leaving the DB in an inconsistent
        # state by design -- since the NOKO records could change outside of this
        # code -- if it fails, you should reload everything
        #
        sys.exit("ERROR -- Execute_sql failed")


def execute_ddl(conn,sql_statement):
    """ Execute a DDL statement -- DROP/CREATE/TRUNCATE"""
    try:
        conn.cursor().execute(sql_statement)
        conn.commit()
        #
        # Same logging logic as per the method above
        #
        pg_noko_logger.log("I","EXECUTE_DDL",sql_statement)
        #
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Log the error if the SQL fails
        #
        pg_noko_logger.log("E","EXECUTE_DDL",str(error))
        #
        # This is not very resilient, but we did not want to plumb in
        # logic to re-start where we left off.   If any SQL fails, we
        # report the failure and exit -- leaving the DB in an inconsistent
        # state by design -- since the NOKO records could change outside of this
        # code -- if it fails, you should reload everything
        #
        sys.exit("ERROR -- Execute_ddl failed")
 


