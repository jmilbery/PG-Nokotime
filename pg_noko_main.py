#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Main "contoller" for Noko/PostgreSQL integration
# ---------------------------------------------------------------------------
""" Main Python module for running Noko/PostgreSQL integration """
import sys
import argparse
import pg_noko_api_entries
import pg_noko_api_tags
import pg_noko_api_projects
import pg_noko_logger
import pg_noko_sql
import pg_noko_db
import config


""" Each main function is set as a parameter for the command line """

parser = argparse.ArgumentParser()
parser.add_argument(
    '--noko_entries', 
    help='Fetch ENTRIES from Noko API and load them into PostgreSQL database',
    action="store_true"
    )
parser.add_argument(
    '--noko_tags', 
    help='Fetch TAGS from Noko API and load them into PostgreSQL database',
    action="store_true"
    )
parser.add_argument(
    '--noko_projects', 
    help='Fetch PROJECTS from Noko API and load them into PostgreSQL database',
    action="store_true"
    )
parser.add_argument(
        '--test_db_connection', 
        help='Verify connection to PostgreSQL database',
        action="store_true"
        )
parser.add_argument(
    '--drop_tables', 
    help='Drop Tables in the PostgreSQL database',
    action="store_true"
    )
parser.add_argument(   
    '--create_tables',
    help='Create Tables in the PostgreSQL database',
    action="store_true"
    )
parser.add_argument(
    '--truncate_tables', 
    help='Truncate RAW Tables in the PostgreSQL database',
    action="store_true"
    )
args = parser.parse_args()

""" Core controller, each "--" argument defined by the parser has
    associated entry below.  As currently designed
"""
if args.noko_entries:
    """ Get Entries """
    pg_noko_api_entries.get_entries(config.page_max,config.api_root,config.per_page,config.noko_token)
    sys.exit("SUCCESS:Loaded Noko Entries into PostgreSQL")

if args.noko_tags:
    """ Get Tags """
    pg_noko_api_tags.get_tags(config.page_max,config.api_root,config.per_page,config.noko_token)
    sys.exit("SUCCESS:Loaded Noko Tags into PostgreSQL")

if args.noko_projects:
    """ Get Projects """
    pg_noko_api_projects.get_projects(config.page_max,config.api_root,config.per_page,config.noko_token)
    sys.exit("SUCCESS:Loaded Noko Projects into PostgreSQL")

if args.test_db_connection:
    """ Check DB connection """
    pg_noko_db.test_db_connection()
    sys.exit("SUCCESS:Tested Connection from config.py to PostgreSQL")

if args.drop_tables:
    """ Drop Tables """
    pg_noko_sql.drop_tables()
    sys.exit("SUCCESS:Dropped RAW tables in PostgreSQL")

if args.create_tables:
    """ Create Tables """
    pg_noko_sql.create_tables()
    sys.exit("SUCCESS:Created RAW tables in PostgreSQL")

if args.truncate_tables:
    """ truncate Tables """
    pg_noko_sql.truncate_tables()
    sys.exit("SUCCESS:Truncated RAW tables in PostgreSQL")