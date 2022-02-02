#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Accepts a response block from a Noko Entries API call 
# ---------------------------------------------------------------------------
""" Formats and Calls an API call for Noko ENTRIES called by pg_noko_main """
import requests
from datetime import datetime
import pg_noko_sql
import pg_noko_logger


def get_entries(page_max,api_root,per_page,noko_token):
    """ Format and call Noko ENTRIES api call with paging paramters """

    # Start at first page, call API to page max
    for page in range(1,int(page_max)):
        #
        # Create API string from INI variables
        #
        api_url = api_root +"entries?"+ "per_page=" + per_page + "&" + "noko_token=" + noko_token + "&page="+str(page)
        pg_noko_logger("I", api_url)
        response = requests.get(api_url)
        #
        # Process response, return when the API returns a null packet
        #
        if response.text.strip() == "[]":
            return
        else:
            process_entries(response)


def process_entries(response):
    """ Process the JSON packet that is returned from Noko API call """
    data = response.json()
    #
    # For each JSON "record" -- extract the desired elements (take a look at the Noko API
    # docs to understand the JSON format)
    #
    for jline in data:
        # record id
        noko_entry_id = str(jline['id'])
        # user
        noko_user =  jline['user']['email'].upper()
        # Date
        noko_date = str(jline['date']).upper()
        # minutes
        noko_minutes = str(jline['minutes'])
        # description
        noko_desc = jline['description'].replace(",","").upper()
        #
        # It's possible to have a null project, so we try to extract the name,
        # but if it fails, we force it to "N/A"
        try:
            noko_project_name = jline['project']['name'].upper()
        except:
            noko_project_name = "N/A"
        #
        # Pass the extracted values to a module to create the insert SQL string
        #
        pg_noko_sql.insert_noko_raw_entries(noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc)
        return
        
