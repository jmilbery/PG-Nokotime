#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Main "contoller" for Noko/PostgreSQL integration
# ---------------------------------------------------------------------------
""" Main Python module for running Noko/PostgreSQL integration """
import sys
import argparse
import pg_noko_api_entries
import pg_noko_sql
import pg_noko_db
import config
import pg_noko_dates

#
# This is the main program - it quarterbacks everything else.  All "commands"
# are command-line functions.  Use the following execution string to show the options:
#
# python3 pg_noko_main.py --help
#
# Each function is matched as a parameter for the command line using the python
# argparse library

parser = argparse.ArgumentParser()
#
# Test the connection to the database, without fetching NOKO API
# data or updating the database.   
#
parser.add_argument(
        '--test_db_connection', 
        help='Verify connection to PostgreSQL database',
        action="store_true"
        )
#
# Drop the noko_entries, noko_projects, noko_tags and noko_entries_tags
# tables
#
parser.add_argument(
    '--drop_tables', 
    help='Drop Tables in the PostgreSQL database',
    action="store_true"
    )
#
# Create the noko_entries, noko_projects, noko_tags and noko_entries_tags
# tables
#
parser.add_argument(   
    '--create_tables',
    help='Create Tables in the PostgreSQL database',
    action="store_true"
    )
#
# Truncate the noko_entries, noko_projects, noko_tags and noko_entries_tags
# (Deletes all the data)
#
parser.add_argument(
    '--truncate_tables', 
    help='Truncate Noko Tables in the PostgreSQL database',
    action="store_true"
    )
#
# Add foreign keys
#
parser.add_argument(
    '--add_foreign_keys', 
    help='Add foreign keys to PostgreSQL database tables (use after loading all data)',
    action="store_true"
    )
#
# Call the Noko ENTRIES API and fetch entry, project and tag data
#
parser.add_argument(
    '--noko_api_entries', 
    help='Fetch ENTRIES from Noko API and load them into PostgreSQL database',
    action="store_true"
    )
#
# Drop and re-create ONLY the noko_dates table
#
parser.add_argument(
    '--noko_dates', 
    help='Drop/Create Noko_dates table in the PostgreSQL database and load it',
    action="store_true"
    )
args = parser.parse_args()
#
# Each entry here matches an argparse argument list defined above
#
if args.noko_api_entries:
    """ Get Entries """
    pg_noko_api_entries.get_entries(config.api_root,config.per_page,config.noko_token)
    sys.exit("SUCCESS:Loaded Noko Entries into PostgreSQL")

if args.test_db_connection:
    """ Check DB connection """
    conn = pg_noko_db.connect_db()
    sys.exit("SUCCESS:Tested Connection from config.py to PostgreSQL ["+config.host+"/"+config.dbname+"]")

if args.drop_tables:
    """ Drop Tables """
    pg_noko_sql.drop_tables()
    sys.exit("SUCCESS:Dropped tables in PostgreSQL")

if args.create_tables:
    """ Create Tables """
    pg_noko_sql.create_tables()
    sys.exit("SUCCESS:Created tables in PostgreSQL")

if args.truncate_tables:
    """ truncate Tables """
    pg_noko_sql.truncate_tables()
    sys.exit("SUCCESS:Truncated tables in PostgreSQL")

if args.add_foreign_keys:
    """ add foreign keys to tables  """
    pg_noko_sql.add_foreign_keys()
    sys.exit("SUCCESS:Add foreign keys and indexes to tables in PostgreSQL")


if args.noko_dates:
    """ Drop/create noko_dates and load it """
    #
    # Drop and create table
    #
    conn = pg_noko_db.connect_db()
    pg_noko_dates.create_noko_dates(conn)
    conn.commit()
    #
    # Load the dates -- stop/start dates defined in config.py
    #
    pg_noko_dates.generate_dates(conn)
    conn.commit()
    #
    sys.exit("SUCCESS:Drop/Create/Load Noko_dates in PostgreSQL")
    