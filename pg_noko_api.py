#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Accepts a response block from a Noko Entries API call and processes the records for loading into DB tables.
# ---------------------------------------------------------------------------

import requests

""" Read the pg_noko.ini file"""


def get_entries(page_max,api_root,per_page,noko_token):
    num_records = 0    

    for page in range(1,int(page_max)):
        # Combine preceeding variables for initial 
        api_url = api_root + "per_page=" + per_page + "&" + "noko_token=" + noko_token + "&page="+str(page)
        response = requests.get(api_url)
        #print (response.text.strip())
        if response.text.strip() == "[]":
            quit()
        else:
            process_response(response)


def process_response(response):
    data = response.json()
    strOutline = ""
    for jline in data:
        # record id
        strOutline  = strOutline + str(jline['id'])
        # user
        strOutline = strOutline + ',' + jline['user']['email']
        # Date
        strOutline = strOutline + ',' + str(jline['date'])
        # minutes
        strOutline = strOutline + ',' + str(jline['minutes'])
        # description
        strOutline  = strOutline + ','+jline['description'].replace(",","")
        try:
            #print(jline['project']['name'])
            strOutline = strOutline + ',' + jline['project']['name']
        except:
            strOutline = strOutline + ',' +"N/A"
        if len(strOutline.strip()) > 0:
            strOutline = strOutline.replace('\r', '')
            strOutline = strOutline.replace('\n', '')
            #print (strOutline.upper())
        strOutline=""
