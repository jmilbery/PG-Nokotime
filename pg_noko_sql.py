#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Creates/formats SQL statements for the PostgreSQL database
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the PostgreSQL database """
import sys
from datetime import datetime
import psycopg2
import pg_noko_db
import pg_noko_logger
import pg_sql_noko_entries_tags
import pg_sql_noko_entries
import pg_sql_noko_tags
import pg_sql_noko_projects


def create_tables():
    """ Create the database tables """
    #
    # Create the tables
    #
    try:
        conn = pg_noko_db.connect_db()
        pg_noko_db.execute_ddl(conn,pg_sql_noko_entries_tags.create_noko_entries_tags)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_entries.create_noko_entries)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_tags.create_noko_tags)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_projects.create_noko_projects)
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Log the error if the SQL fails
        #
        pg_noko_db.close_db(conn)
        pg_noko_logger.log("E","EXECUTE_SQL - CREATE:",str(error))
        #
    # Commit the changes and close the db connection
    #
    conn.commit()
    pg_noko_db.close_db(conn)
    #
def drop_tables():
    """ Drop the database tables """
    #
    # Drop Tables
    #
    try:
        conn = pg_noko_db.connect_db()
        pg_noko_db.execute_ddl(conn,pg_sql_noko_entries_tags.drop_noko_entries_tags)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_entries.drop_noko_entries)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_tags.drop_noko_tags)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_projects.drop_noko_projects)
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Log the error if the SQL fails
        #
        pg_noko_db.close_db(conn)
        pg_noko_logger.log("E","EXECUTE_SQL - DROP:",str(error))
        #
    # Commit the changes and close the db connection
    #
    conn.commit()
    pg_noko_db.close_db(conn)   
#
#   Create core tables
#

def truncate_tables():
    """ Truncate (delete all records from a table) """
    #
    try:
        conn = pg_noko_db.connect_db()
        pg_noko_db.execute_ddl(conn,pg_sql_noko_entries_tags.truncate_noko_entries_tags)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_entries.truncate_noko_entries)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_tags.truncate_noko_tags)
        pg_noko_db.execute_ddl(conn,pg_sql_noko_projects.truncate_noko_projects)
    except (Exception, psycopg2.DatabaseError) as error:
        #
        # Log the error if the SQL fails
        #
        pg_noko_db.close_db(conn)
        pg_noko_logger.log("E","EXECUTE_SQL - TRUNCATE:",str(error))
        #
    # Commit the changes and close the db connection
    #
    conn.commit()
    pg_noko_db.close_db(conn)
    #
 
 

