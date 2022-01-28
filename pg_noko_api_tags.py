#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Accepts a response block from a Noko Entries API call and processes the records for loading into DB tables.
# ---------------------------------------------------------------------------

import requests

""" Read the pg_noko.ini file"""


def get_tags(page_max,api_root,per_page,noko_token):
    num_records = 0    

    for page in range(1,int(page_max)):
        # Combine preceeding variables for initial 
        api_url = api_root + "tags?"+ "per_page=" + per_page + "&" + "noko_token=" + noko_token + "&page="+str(page)
        response = requests.get(api_url)
        #print (response.text.strip())
        if response.text.strip() == "[]":
            quit()
        else:
            process_tags(response)


def process_tags(response):
    data = response.json()
    strOutline = ""
    for jline in data:
        # record id
        strOutline  = strOutline + str(jline['id'])
        # Name (no hash)
        strOutline = strOutline + ',' + jline['name']
        # Formatted name (with hash)
        strOutline = strOutline + ',' + str(jline['formatted_name'])
        # Billable flag
        strOutline = strOutline + ',' + str(jline['billable'])
        if len(strOutline.strip()) > 0:
            strOutline = strOutline.replace('\r', '')
            strOutline = strOutline.replace('\n', '')
            print (strOutline.upper())
        strOutline=""
