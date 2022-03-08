#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Library to connect to the PostgreSQL database via psycopg2 and execute SQL
# ---------------------------------------------------------------------------
""" Library to connect to the PostgreSQL database via psycopg2 and execute SQL"""
import psycopg2
import psycopg2.extras as psycopg2_extras
import sys
import pg_noko_logger
import config
#
#
# Create the db connection string from fields in the config.py library
#
def connect_db():
    """ Connect to PostgreSQL using the parameters from config.sys and
    return the connection to the caller.  This isolates the database login
    information to a single module.
    """
    try:
        conn = psycopg2.connect(dbname=config.dbname, user=config.user, 
        password=config.password,host=config.host, port=config.port)
        conn.cursor().execute("""SELECT user""")
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Failing to make a DB connection is a fatal error for this
        # code, so exit
        #
        pg_noko_logger.log("E","Connect_db() failed: ",str(error))
        sys.exit("FATAL ERROR -- connect_db() failed: "+str(error))
    #
    # Return the open db connection
    #
    return conn

def close_db(conn):
    """ Disconnect from the PostgreSQL database.  You could simply use
        conn.close() in the calling program, but we provide this routine
        in the event that you want to execute some custom logic before
        disconnecting
    """
    try:
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        pg_noko_logger.log("E","close_db() failed: ",str(error))
        sys.exit("FATAL ERROR -- close_db() failed: "+str(error))

def execute_sql(conn,sql_statement, data):
    """ Execute a DELETE/UPDATE/INSERT SQL statement.  This routine only
        runs SQL Delete/Update/Insert commands -- it will not work for
        fetching data, as there are no cursors in this routine
    """
    #
    # Pass the SQL string in psycopg2 format and the column data
    # as a python list
    #
    try:
        #
        # Very simple logging, we did not bother with the python logging
        # library which is much more comprehensive.   We pass the SQL
        # statement and the data to the log method.   If config.py has
        # log_sql set to true, it will output the data to stdout.
        #
        # Use the mogrify method to create the full SQL statment (including data)
        query = conn.cursor().mogrify(sql_statement,data)
        pg_noko_logger.log_sql(query)
        #
        # Execute the query
        #
        conn.cursor().execute(sql_statement,data)
        conn.commit()
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
        # code -- if it fails, you should reload everything.
        #
        sys.exit("ERROR -- Execute_sql failed")

def execute_batch_sql(conn,sql_statement, data):
    """ Execute a BATCH DELETE/UPDATE/INSERT SQL statement.  This routine only
        runs SQL Delete/Update/Insert commands -- this routine takes an
        SQL statement and a list of lists -- and sends them to the database in
        a batch - which is much faster than the singleton 'execute_sql'
    """
    #
    # Pass the SQL string in psycopg2 format and the column data
    # as a python list
    #
    try:
        #
        # Very simple logging, we did not bother with the python logging
        # library which is much more comprehensive.   We pass the SQL
        # statement and the data to the log_sql method.   If config.py has
        # log_SQL set to true, it will output the data to stdout.
        #
        # 
        # For BATCH executions (much faster for lots of records),
        # then we iterate over the list of lists to create individual
        # queries for logging.
        #
        for list in data:
            query = conn.cursor().mogrify(sql_statement,list)
            pg_noko_logger.log_sql(query)
        #
        #
        # Run the query
        #
        cur = conn.cursor()
        psycopg2_extras.execute_batch(cur, sql_statement, data, page_size=100)        
        conn.commit()
        #
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Log the error if the SQL fails
        #
        pg_noko_logger.log("E","EXECUTE_BATCH_SQL",str(error))
        #
        # This is not very resilient, but we did not want to plumb in
        # logic to re-start where we left off.   If any SQL fails, we
        # report the failure and exit -- leaving the DB in an inconsistent
        # state by design -- since the NOKO records could change outside of this
        # code -- if it fails, you should reload everything
        #
        sys.exit("ERROR -- Execute_batch_sql failed")

def execute_ddl(conn,sql_statement):
    """ Execute a DDL statement -- DROP/CREATE/TRUNCATE.  You could use the
        execute_sql routine to run DML commands to the database.  I've added
        this routine for future extensions.
    """
    try:
        #
        # Same logging logic as per the method above (execute_sql)
        #
        query = conn.cursor().mogrify(sql_statement)
        pg_noko_logger.log_sql(query)
        #
        # Execute the query
        #
        conn.cursor().execute(sql_statement)
        conn.commit()
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
        # code -- if it fails, you should reload everything.
        #
        sys.exit("ERROR -- Execute_ddl failed")


