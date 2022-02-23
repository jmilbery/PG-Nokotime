#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Sample config.py file for configuration variables - rename to config.py
# ---------------------------------------------------------------------------
""" Stores confiuguration variables """
#
# Noko API settings
#
per_page = 100
api_root = "https://api.nokotime.com/v2/"
noko_token = "xxxxxxx"
#
# PostgreSQL database variables
#
dbname="postgres"
user="pguser"
password="pgpwd"
host="localhost"
port=5433
schema="noko"
#
# Set variable for outputting messages to stdout
#
log_message=True
#
# Start/End dates for noko_dates table
#
start_date="2018-01-01"
end_date="2022-12-31"