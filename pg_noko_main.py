#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Main "contoller" for Noko/PostgreSQL integration
# ---------------------------------------------------------------------------
""" Main Python module for running Noko/PostgreSQL integration """
import sys
import argparse
from configparser import ConfigParser
import pg_noko_api_entries
import pg_noko_api_tags
import pg_noko_api_projects
import pg_noko_logger


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

""" Read the pg_noko.ini configuration file to get NOKO API parameters and PostgreSQL DB parameters"""
""" sample.ini has entries and examples for every required parameter """
try:
    configur = ConfigParser()
    configur.read('pg_noko.ini')
    per_page = configur.get('noko','per_page')
    page_max = configur.get('noko','page_max')
    api_root = configur.get('noko','api_root')
    noko_token = configur.get('noko','noko_token')
except:
    pg_noko_logger.log("I","Missing Noko INI Setting/Value")
    sys.exit("ERROR: Missing value in INI file")

""" Core controller, each "--" argument defined by the parser has
    associated entry below.  As currently designed
"""
if args.noko_entries:
    """ Get Entries """
    pg_noko_api_entries.get_entries(page_max,api_root,per_page,noko_token)
    sys.exit("SUCCESS:Loaded Noko Entries into PostgreSQL")

if args.noko_tags:
    """ Get Tags """
    pg_noko_api_tags.get_tags(page_max,api_root,per_page,noko_token)
    sys.exit("SUCCESS:Loaded Noko Tags into PostgreSQL")

if args.noko_projects:
    """ Get Projects """
    pg_noko_api_projects.get_projects(page_max,api_root,per_page,noko_token)
    sys.exit("SUCCESS:Loaded Noko Projects into PostgreSQL")

if args.test_db_connection:
    """ Check DB connection """
    pg_noko_sql.test_db_connection()
    sys.exit("SUCCESS:Tested Connection from INI file to PostgreSQL")

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
    pg_noko_sql.truncate_table("noko_raw_entries")
    pg_noko_sql.truncate_table("noko_raw_tags")
    pg_noko_sql.truncate_table("noko_raw_projects")
    sys.exit("SUCCESS:Truncated RAW tables in PostgreSQL")