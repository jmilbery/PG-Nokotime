#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Creates/format SQL for the PostgreSQL database
# ---------------------------------------------------------------------------
import sys
from datetime import datetime
import pg_noko_db
import pg_noko_logger
import config
#
# Generate a "date stamp in the format YYYY-MM-DD
#
now = datetime.now() 
load_date = now.strftime("%Y-%m-%d")

def drop_tables():
    """ Drop the three core tables, noko_entries, noko_tags and noko_projects"""
    #
    # Create drop string for noko_entries and pass to DB for execution
    #
    sql_drop_noko_entries = "drop table if exists "+ config.schema+ ".noko_entries cascade"
    pg_noko_db.execute_ddl(sql_drop_noko_entries)
    #
    # Create drop string for noko_tags and pass to DB for execution
    #
    sql_drop_noko_tags = "drop table if exists "+ config.schema+ ".noko_tags cascade"
    pg_noko_db.execute_ddl(sql_drop_noko_tags)
    #
    # Create drop string for noko_projects and pass to DB for execution
    #
    sql_drop_noko_projects = "drop table if exists "+ config.schema + ".noko_projects cascade"
    pg_noko_db.execute_ddl(sql_drop_noko_projects)
    #
    # Create drop string for noko_entry_tag and pass to DB
    sql_drop_noko_entry_tag = "drop table if exists " + config.schema + ".noko_entries_tags"
    pg_noko_db.execute_ddl(sql_drop_noko_entry_tag)
    #
    # Create drop string for noko_dates
    sql_drop_noko_dates = "drop table if exists "+ config.schema + ".noko_dates"
    pg_noko_db.execute_ddl(sql_drop_noko_dates)

#   Create core tables
#
def create_tables():
    """ Create the three core tables, noko_entries, noko_tags and noko_projects"""

    # PostgreSQL schema name is stored in the INI file, we plumb it in here.
    #
    # Create the table to store ENTRY records from Noko
    #
    sql_create_noko_entries = "CREATE TABLE "+ config.schema + """.noko_entries (
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
    pg_noko_db.execute_ddl(sql_create_noko_entries)
    #
    # Create the table to store TAGS records from Noko
    #
    sql_create_noko_tags = "CREATE TABLE "+ config.schema + """.noko_tags
    (noko_tag_id int8 NOT NULL,
    noko_tag_name varchar(128),
    noko_tag_formatted varchar(128),
    noko_tag_billable bool,
    load_date date,
    PRIMARY KEY (noko_tag_id))"""
    pg_noko_db.execute_ddl(sql_create_noko_tags)
    #
    # Create the table to store PROJECTS records from Noko
    #
    sql_create_noko_projects = "CREATE TABLE " + config.schema + """.noko_projects
    (noko_project_id bigint NOT NULL,
    noko_project_name varchar(128),
    noko_description varchar(1024),
    noko_enabled bool,
    noko_billable bool,
    load_date date,
    PRIMARY KEY (noko_project_id))"""
    pg_noko_db.execute_ddl(sql_create_noko_projects)
    #
    # Create production entry/tag table
    sql_create_noko_entries_tags = "CREATE TABLE " + config.schema + """.noko_entries_tags
    (noko_tag_id int8 NOT NULL,
    noko_entry_id int8 NOT NULL,
    load_date date,
    PRIMARY KEY (noko_tag_id, noko_entry_id))"""
    pg_noko_db.execute_ddl(sql_create_noko_entries_tags)
    #
    # Create production datestable
    sql_create_noko_dates = "CREATE TABLE " + config.schema + """.noko_dates
    (noko_date date,
    noko_day_of_week char(3),
    noko_week_of_year int2,
    noko_month int,
    noko_year int4,
    noko_day_of_month int4,
    noko_day_of_year int2,
    noko_quarter char(2),
    load_date date,
    primary key (noko_date))"""
    pg_noko_db.execute_ddl(sql_create_noko_dates)

def truncate_tables():
    """ Truncate (delete all records from a table) """
    sql_command = "truncate table " + config.schema + ".noko_tags cascade"
    pg_noko_db.execute_ddl(sql_command)

    sql_command = "truncate table " + config.schema + ".noko_projects cascade"
    pg_noko_db.execute_ddl(sql_command)

    sql_command = "truncate table " + config.schema + ".noko_entries cascade"
    pg_noko_db.execute_ddl(sql_command)

    sql_command = "truncate table " + config.schema + ".noko_entries_tags cascade"
    pg_noko_db.execute_ddl(sql_command)

    sql_command = "truncate table " + config.schema + ".noko_dates cascade"
    pg_noko_db.execute_ddl(sql_command)

def insert_noko_tags(noko_tag_id, noko_tag_name, noko_tag_formatted, noko_tag_billable):
    """ SQL Insert string for TAGS data.  Insert string is a fixed format """
    sql_insert = ("insert into " 
        + config.schema
        + ".noko_tags (noko_tag_id, noko_tag_name,noko_tag_formatted, noko_tag_billable, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s) on conflict do nothing"
    #
    # Package the insert variables into a list
    #
    sql_data = [noko_tag_id, noko_tag_name,noko_tag_formatted, noko_tag_billable, load_date]
    #
    # Pass the insert statement and the variables (via a list) to function to execute the DB
    #
    pg_noko_db.execute_sql(sql_insert, sql_data)

def insert_noko_entries(noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc):
    """ SQL Insert for ENTRIES data"""
    sql_insert = ("insert into "
    + config.schema
    + ".noko_entries (noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s, %s, %s) on conflict do nothing"
    sql_data = [noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc, load_date]
    pg_noko_db.execute_sql(sql_insert, sql_data)

def insert_noko_projects(noko_project_id, noko_project_name, noko_enabled, noko_billable):
    """ SQL Insert for PROJECTS data """
    sql_insert = ("insert into "
    + config.schema
    + ".noko_projects (noko_project_id, noko_project_name, noko_enabled, noko_billable, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s) on conflict do nothing"
    sql_data = [noko_project_id, noko_project_name, noko_enabled, noko_billable, load_date]
    pg_noko_db.execute_sql(sql_insert, sql_data)

def insert_noko_entries_tags(noko_tag_id, noko_entry_id):
    """ SQL Insert for Entries_tags data """
    sql_insert = ("insert into "
    + config.schema
    + ".noko_entries_tags (noko_entry_id, noko_tag_id, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s) on conflict do nothing"
    sql_data = [noko_entry_id, noko_tag_id, load_date]
    pg_noko_db.execute_sql(sql_insert, sql_data)

def insert_noko_dates(noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter):
    """ SQL Insert string for DATES data.  Insert string is a fixed format """
    sql_insert = ("insert into " 
        + config.schema
        + ".noko_dates (noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s, %s, %s, %s, %s) on conflict do nothing"
    #
    # Package the insert variables into a list
    #
    sql_data = [noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter]
    #
    # Pass the insert statement and the variables (via a list) to function to execute the DB
    #
    pg_noko_db.execute_sql(sql_insert, sql_data)
