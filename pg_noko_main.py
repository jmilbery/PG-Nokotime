#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Usage python3 pg_noko_main.py
# ---------------------------------------------------------------------------

import sys
import pg_noko_api
import pg_noko_db
import pg_noko_logger
import argparse
from configparser import ConfigParser


parser = argparse.ArgumentParser()
parser.add_argument('--noko_entries', help='Fetch ENTRIES from Noko API and load them into PostgreSQL database',action="store_true")
parser.add_argument('--test_db_connection', help='Verify connection to PostgreSQL database',action="store_true")
parser.add_argument('--drop_tables', help='Drop Tables in the PostgreSQL database',action="store_true")
args = parser.parse_args()

""" Read the pg_noko.ini configuration file to get NOKO API parameters and PostgreSQL DB parameters"""

try:
    configur = ConfigParser()
    configur.read('pg_noko.ini')
    per_page = configur.get('noko','per_page')
    page_max = configur.get('noko','page_max')
    api_root = configur.get('noko','api_root')
    noko_token = configur.get('noko','noko_token')
except:
    pg_noko_logger.log("I","Missing Noko INI Settings")
    quit()

if args.noko_entries:
    """ Get Entries """
    pg_noko_api.get_entries(page_max,api_root,per_page,noko_token)

if args.test_db_connection:
    """ Check DB connection """
    pg_noko_db.test_db_connection()
    quit()

if args.drop_tables:
    """ Drop Tables """
    pg_noko_db.drop_tables()
    quit()
