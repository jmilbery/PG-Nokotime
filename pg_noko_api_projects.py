#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# version ='1.0'
# Accepts a response block from a Noko Projects API call and processes the records for loading into DB tables.
# ---------------------------------------------------------------------------

import requests
import pg_noko_sql
from datetime import datetime

def get_projects(page_max,api_root,per_page,noko_token):
    """ Format API string and call Noko PROJECTS API call"""

    # Start at first page, call API to page max
    #
    for page in range(1,int(page_max)):
        #
        # Combine INI variables into URL string
        #
        api_url = api_root +"projects?"+ "per_page=" + per_page + "&" + "noko_token=" + noko_token + "&page="+str(page)
        response = requests.get(api_url)
        #
        # Process response, return when the API returns a null packet
        #
        if response.text.strip() == "[]":
            return
        else:
            process_projects(response)


def process_projects(response):
    """ Process the JSON packet that is returned from Noko API call """
    data = response.json()
    #
    # For each JSON "record" -- extract the desired elements (take a look at the Noko API
    # docs to understand the JSON format)
    #
    for jline in data:
        # record id
        noko_project_id = str(jline['id'])
        # project name
        noko_project_name =  jline['name'].upper()
        # description
        noko_description = str(jline['description']).upper()
        # enabled
        noko_enabled = jline['enabled']
        # billable
        noko_billable = jline['billable']
        #
        # Pass the extracted values to a module to create the insert SQL string
        #
        pg_noko_sql.insert_noko_raw_projects(noko_project_id, noko_project_name, noko_description, noko_enabled, noko_billable)
        return
