#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Generates a set of date records for Noko Tables to allow for simpler SQL
# ---------------------------------------------------------------------------
""" Generates a set of date records for Noko Tables 
    This module has a slightly different format from
    the other database table code.  All of the logic
    (including the SQL queries) is stored in-line in this
    routine -- making it easier to run it standalone
"""
from datetime import timedelta
from datetime import date
from datetime import datetime
import config
import pg_noko_db
import pg_sql_noko_dates

#
# Generate a "date stamp in the format YYYY-MM-DD that we'll use for the load_date
# field in the database -- so we'll know when this table is loaded and created.
#
now = datetime.now() 
load_date = now.strftime("%Y-%m-%d")

def create_noko_dates(conn):
    """ Drop and create the noko_dates table
     Create drop/create SQL commands for noko_dates table.  We've isolated the drop/create/load
     functions into this library so that you can load the dates table independently from
     the other noko tables.  (You might want to pull all entries and then decide on the
     range for your noko_dates table).  Noko_dates should be loaded BEFORE you add the
     foreign keys """
    #
    # Drop the dates table.  PostgreSQL uses "schemas", which we pull from the config.py
    # library
    #
    pg_noko_db.execute_ddl(conn,pg_sql_noko_dates.drop_noko_dates)
    #
    # Create production noko_dates table. PostgreSQL uses "schemas", which we pull from the config.py
    # library
    #
    pg_noko_db.execute_ddl(conn,pg_sql_noko_dates.create_noko_dates)

def generate_dates(conn):
    """ Generate dates records using a range from config.py
     This method creates the fields for a date record that match the PostgreSQL
     table fields.  Essentially, we take a date and pull out a variety of elements,
     such as day of the week, quarter of the year, etc -- the Noko_entries will join
     this table on the noko_date field -- and then you can use the elements of the noko_date
     record to extract entries (or group them) by date elements -- for example -- finding
     all entries that occur on a "Monday", or in a given quarter. 
     Start and end dates are stored in the config.py library """
    #
    start = datetime.strptime(config.start_date, "%Y-%m-%d")
    end =   datetime.strptime(config.end_date, "%Y-%m-%d")
    # 
    # Calculate the difference (in days) between the start and end
    # dates in days for the loop length.
    # 
    diff = end.date() - start.date()
    #
    # Create an empty list to hold the generated dates
    #
    noko_dates_list = []
    #
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
        # Calculate the "quarter" of the calendar year and
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
        # Add the current row to the list, creating a list of lists that we can
        # pass to the DB as a batch
        #
        noko_current_date = [noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter,load_date]
        noko_dates_list.append(noko_current_date)
    
    # End of loop creating the dates list of lists.
    # pass the connection, insert statement string and list to the pg_noko_db for executing
    # against the db
    #
    pg_noko_db.execute_batch_sql(conn,pg_sql_noko_dates.insert_noko_dates, noko_dates_list)

