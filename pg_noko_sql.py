#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Creates/format SQL for the PostgreSQL database
# ---------------------------------------------------------------------------
import sys
from configparser import ConfigParser
from datetime import datetime
import pg_noko_db
import pg_noko_logger

""" Read the pg_noko.ini configuration file to get the name of the PostgreSQL schema to use"""
try:
    configur = ConfigParser()
    configur.read('pg_noko.ini')
    ini_schema = configur.get('db','schema')
except:
    pg_noko_logger.log("E","Missing PostgreSQL SCHEMA INI Settings")
    sys.exit("ERROR: Missing PostgreSQL schema string")

#
# Generate a "date stamp in the format YYYY-MM-DD
#
now = datetime.now() 
load_date = now.strftime("%Y-%m-%d")

def drop_tables():
    """ Drop the three core tables, noko_raw_entries, noko_raw_tags and noko_raw_projects"""
    #
    # Create drop string for noko_raw_entries and pass to DB for execution
    #
    sql_drop_noko_raw_entries = "drop table if exists "+ ini_schema+ ".noko_raw_entries cascade"
    pg_noko_db.execute_ddl(sql_drop_noko_raw_entries)
    #
    # Create drop string for noko_raw_tags and pass to DB for execution
    #
    sql_drop_noko_raw_tags = "drop table if exists "+ ini_schema+ ".noko_raw_tags cascade"
    pg_noko_db.execute_ddl(sql_drop_noko_raw_tags)
    #
    # Create drop string for noko_raw_projects and pass to DB for execution
    #
    sql_drop_noko_raw_projects = "drop table if exists "+ ini_schema + ".noko_raw_projects cascade"
    pg_noko_db.execute_ddl(sql_drop_noko_raw_projects)

#   Create core tables
#
def create_tables():
    """ Create the three core tables, noko_raw_entries, noko_raw_tags and noko_raw_projects"""

    # PostgreSQL schema name is stored in the INI file, we plumb it in here.
    #
    # Create the table to store ENTRY records from Noko
    #
    sql_create_noko_raw_entries = "CREATE TABLE "+ ini_schema + """.noko_raw_entries (
	noko_entry_id bigint NOT NULL,
    noko_project_name varchar(128),
	noko_user varchar(512),
	noko_date date,
	noko_minutes integer,
	noko_desc varchar(2048),
	load_date date,
	PRIMARY KEY (noko_entry_id)
    );
    """
    pg_noko_db.execute_ddl(sql_create_noko_raw_entries)
    #
    # Create the table to store TAGS records from Noko
    #
    sql_create_noko_raw_tags = "CREATE TABLE "+ ini_schema + """.noko_raw_tags
    (noko_tag_id int8 NOT NULL,
    noko_tag_unformatted varchar(128),
    noko_tag_formatted varchar(128),
    noko_tag_billable bool,
    load_date date,
    PRIMARY KEY (noko_tag_id))"""
    pg_noko_db.execute_ddl(sql_create_noko_raw_tags)
    #
    # Create the table to store PROJECTS records from Noko
    #
    sql_create_noko_raw_projects = "CREATE TABLE " + ini_schema + """.noko_raw_projects
    (noko_project_id bigint NOT NULL,
    noko_project_name varchar(128),
    noko_description varchar(1024),
    noko_enabled bool,
    noko_billable bool,
    load_date date,
    PRIMARY KEY (noko_project_id))"""
    pg_noko_db.execute_ddl(sql_create_noko_raw_projects)

def truncate_table(table_name):
    """ Truncate (delete all records from a table) """
    sql_command = "truncate table " + ini_schema + "." + table_name + " cascade"
    pg_noko_db.execute_sql(sql_command)

def insert_noko_raw_tags(noko_tag_id, noko_tag_unformatted, noko_tag_formatted, noko_tag_billable):
    """ SQL Insert string for TAGS data.  Insert string is a fixed format """
    sql_insert = ("insert into " 
        + ini_schema
        + ".noko_raw_tags (noko_tag_id, noko_tag_formatted,noko_tag_unformatted, noko_tag_billable, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s)"
    #
    # Package the insert variables into a list
    #
    sql_data = [noko_tag_id, noko_tag_formatted,noko_tag_unformatted, noko_tag_billable, load_date]
    #
    # Pass the insert statement and the variables (via a list) to function to execute the DB
    #
    pg_noko_db.execute_sql(sql_insert, sql_data)

def insert_noko_raw_entries(noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc):
    """ SQL Insert for ENTRIES data"""
    sql_insert = ("insert into "
    + ini_schema
    + ".noko_raw_entries (noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s, %s, %s)"
    sql_data = [noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc, load_date]
    pg_noko_db.execute_sql(sql_insert, sql_data)

def insert_noko_raw_projects(noko_project_id, noko_project_name, noko_description, noko_enabled, noko_billable):
    """ SQL Insert for PROJECTS data """
    sql_insert = ("insert into "
    + ini_schema
    + ".noko_raw_projects (noko_project_id, noko_project_name, noko_description, noko_enabled, noko_billable, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s, %s)"
    sql_data = [noko_project_id, noko_project_name, noko_description, noko_enabled, noko_billable, load_date]
    pg_noko_db.execute_sql(sql_insert, sql_data)



