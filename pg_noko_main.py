#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Usage python3 pg_noko_main.py [noko api key]
# ---------------------------------------------------------------------------
import requests
import sys
import pg_noko_process_response

"""Set core variables for accessing data"""
# Rows per page fetch
per_page = "100"
# Maximum number of pages to try
page_max = "5000"
# Root Noko API for time entries
api_root = "https://api.nokotime.com/v2/entries?"
# Noko token for access
noko_token = ""
#
num_records = 0
#
# Open local file and fetch Noko Api Key
#
try:
    noko_token = sys.argv[1]
except:
    print("ERROR -- NOKO API KEY not passed on the command line ")
    quit()


for page in range(1,int(page_max)):
    # Combine preceeding variables for initial 
    api_url = api_root + "per_page=" + per_page + "&" + "noko_token=" + noko_token + "&page="+str(page)
    response = requests.get(api_url)
    #print (response.text.strip())
    if response.text.strip() == "[]":
        quit()
    else:
        pg_noko_process_response.process_response(response)