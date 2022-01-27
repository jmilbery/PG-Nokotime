#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Logger
# ---------------------------------------------------------------------------
import logging
import sys
logging.basicConfig(format='PG_NOKO_DB:%(process)d-%(levelname)s-%(message)s',stream = sys.stdout, level=logging.INFO)

def log(level, message_string):
    if level == "E":
        logging.error(message_string)
    else:
        logging.info(message_string)