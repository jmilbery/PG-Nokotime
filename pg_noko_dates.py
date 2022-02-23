#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Generates a set of date records for Noko Tables to allow for simpler SQL
# ---------------------------------------------------------------------------
""" Generates a set of date records for Noko Tables """

from datetime import timedelta
from datetime import date
from datetime import datetime
import config
import pg_noko_db

#
# Generate a "date stamp in the format YYYY-MM-DD that we'll use for the load_date
# field in the database -- so we'll know when this table is loaded and created.
#
now = datetime.now() 
load_date = now.strftime("%Y-%m-%d")

def create_noko_dates(conn):
    """ Drop and create the noko_dates table """
    #
    # Create drop string for noko_dates table.  We've isolated the drop/create/load
    # functions into this library so that you can load the dates table independently from
    # the other noko tables.  (You might want to pull all entries and then decide on the
    # range for your noko_dates table)
    #
    # Drop the dates table.  PostgreSQL uses "schemas", which we pull from the config.py
    # library
    #
    sql_drop_noko_dates = "drop table if exists "+ config.schema + ".noko_dates"
    #
    # Call the method in the pg_noko_db library for processing DDLs
    #
    pg_noko_db.execute_ddl(conn,sql_drop_noko_dates)
    #
    # Create production noko_dates table. PostgreSQL uses "schemas", which we pull from the config.py
    # library
    #
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
    #
    # Call the method in the pg_noko_db library for processing DDLs
    #
    pg_noko_db.execute_ddl(conn,sql_create_noko_dates)

def insert_noko_dates(conn,noko_date, noko_day_of_week, noko_week_of_year, noko_month, 
    noko_year, noko_day_of_month, noko_day_of_year, noko_quarter):
    """ Generate insert statment for noko_dates table """
    #
    # Build the insert statement for the noko_dates table, using the schema field from the
    # config.py library.  The format of this string matches the requirements of the psycopg2
    # library
    #
    sql_insert = ("insert into " 
        + config.schema
        + ".noko_dates (noko_date, noko_day_of_week, noko_week_of_year, noko_month"
        + ",noko_year, noko_day_of_month, noko_day_of_year, noko_quarter, load_date)")
    sql_insert = sql_insert + " values (%s, %s, %s, %s, %s, %s, %s, %s, %s) on conflict do nothing"
    #
    # Package the insert variables into a list, which we can pass to the method that executes
    # the SQL statement.
    #
    sql_data = [noko_date, noko_day_of_week, noko_week_of_year, noko_month, 
        noko_year, noko_day_of_month, noko_day_of_year, noko_quarter,load_date]
    #
    # Pass the insert statement and the variables (via a list) to function to execute the SQL
    #
    pg_noko_db.execute_sql(conn,sql_insert, sql_data)
    #
def generate_dates(conn):
    """ Generate dates records using a range from config.py"""
    #
    # This method creates the fields for a date record that match the PostgreSQL
    # table fields.  Essentially, we take a date and pull out a variety of elements,
    # such as day of the week, quarter of the year, etc -- the Noko_entries will join
    # this table on the noko_date field -- and then you can use the elements of the noko_date
    # record to extract entries (or group them) by date elements -- for example -- finding
    # all entries that occur on a "Monday", or in a given quarter.
    #
    # Start and end dates are stored in the config.py library
    #
    start = datetime.strptime(config.start_date, "%Y-%m-%d")
    end =   datetime.strptime(config.end_date, "%Y-%m-%d")
    # 
    # Calculate the difference (in days) between the start and end
    # dates for the loop.
    # 
    diff = end.date() - start.date()

    for date_num in range(diff.days+1):
        #
        # Next date is the start date plus the loop number - starting at "0"
        #
        new_date = start + timedelta(days=date_num)
        noko_date = new_date.strftime("%Y-%m-%d")
        #
        # Get the day of week as a three-character string -- MON, TUE, etc.
        #
        noko_day_of_week = new_date.strftime("%a").upper()
        #
        # Get the week of the year as a number - 1:52
        #
        noko_week_of_year = int(new_date.strftime("%W"))
        #
        # Get the month as a number - 1:12
        #
        noko_month = int(new_date.strftime("%-m"))
        #
        # Get the year as a number -- 2018, 2019, etc.
        #
        noko_year = int(new_date.strftime("%Y"))
        #
        # Get the day of the month as a number -  1:31
        #
        noko_day_of_month = int(new_date.strftime("%-d"))
        #
        # Get the day of the year as a number - 1:365
        #
        noko_day_of_year = int(new_date.strftime("%-j"))
        #
        # Calculate the "quarter" of the calendary year and
        # store as string
        #
        if int(noko_month) <4:
            noko_quarter = 'Q1'
        elif int(noko_month) >3 and int(noko_month) <7:
            noko_quarter = 'Q2'
        elif int(noko_month) >6 and int(noko_month) <10:
            noko_quarter = 'Q3'
        else:
            noko_quarter = 'Q4'
        #
        # Pass the date fields to the method that builds the insert statement
        #
        insert_noko_dates(conn,noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter)

