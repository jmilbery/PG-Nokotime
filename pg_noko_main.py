#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Usage python3 pg_noko_main.py
# ---------------------------------------------------------------------------

import sys
import pg_noko_api
import logging
from configparser import ConfigParser

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
logging.info("Calling pg_noko_api.get_entries()")

""" Read the pg_noko.ini configuration file to get NOKO API parameters and PostgreSQL DB parameters"""
try:
    configur = ConfigParser()
    configur.read('pg_noko.ini')
    per_page = configur.get('noko','per_page')
    page_max = configur.get('noko','page_max')
    api_root = configur.get('noko','api_root')
    noko_token = configur.get('noko','noko_token')
except:
    logging.error("Missing Noko INI Settings")
    quit()

""" Get Entries """
pg_noko_api.get_entries(page_max,api_root,per_page,noko_token)