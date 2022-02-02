#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Accepts a response block from a Noko Tags API call and processes the records for loading into DB tables.
# ---------------------------------------------------------------------------

import requests
import pg_noko_sql
from datetime import datetime


def get_tags(page_max,api_root,per_page,noko_token):
    """ Format URL with passed Noko API parameters and call Noko API"""

    #
    # Call the TAGS Api call from 1 to maximum number of pages
    #
    for page in range(1,int(page_max)):
        #
        # Combine INI variables into URL string
        # 
        api_url = api_root + "tags?"+ "per_page=" + per_page + "&" + "noko_token=" + noko_token + "&page="+str(page)
        response = requests.get(api_url)
        #
        # Check for empty return page, and return, otherwise process the data
        #
        if response.text.strip() == "[]":
            return
        else:
            process_tags(response)

def process_tags(response):
    """ Process the response from a Noko TAGS Api call """
    data = response.json()
    #
    # Extract the field Elements from the JSON data
    #
    for jline in data:
        # record id
        noko_tag_id = jline['id']
        # Name (no hash) -- Force uppercase
        #
        noko_tag_unformatted = jline['name'].upper()
        # Formatted name (with hash) -- Force uppercase
        #
        noko_tag_formatted = jline['formatted_name'].upper()
        # Billable flag
        noko_tag_billable= jline['billable']
        #
        # Pass the extracted values to a module to create the insert SQL string
        #
        pg_noko_sql.insert_noko_raw_tags (noko_tag_id, noko_tag_unformatted, noko_tag_formatted, noko_tag_billable)
        return
