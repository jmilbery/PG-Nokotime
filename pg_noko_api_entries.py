#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Accepts a response block from a Noko Entries API call 
# ---------------------------------------------------------------------------
""" Formats and Calls an API call for Noko ENTRIES called by pg_noko_main """
import requests
import sys
from datetime import datetime
import pg_noko_sql
import pg_noko_logger


def get_entries(page_max,api_root,per_page,noko_token):
    """ Format and call Noko ENTRIES api call with paging paramters """

    # Start at first page, call API to page max
    try:
        for page in range(1,page_max):
            #
            # Create API string from INI variables
            #
            api_url = api_root +"entries?"+ "per_page=" + str(per_page) + "&" + "noko_token=" + noko_token + "&page="+str(page)
            response = requests.get(api_url)
            #
            # Process response, return when the API returns a null packet
            #
            if response.text.strip() == "[]":
                return
            else:
                process_entries(response)
    except Exception as e:
        exit_message = "ERROR get_entries " + str(e)
        print(response.text)
        sys.exit(exit_message)


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
        # billable
        noko_billable = jline['billable']
        #
        # It's possible to have a null project, so we try to extract the name,
        # but if it fails, we force it to "N/A"
        try:
            noko_project_name = jline['project']['name'].upper()
            #
            noko_project_id = jline['project']['id']
            # enabled
            noko_enabled = jline['project']['enabled']
            # billable
            noko_billable = jline['project']['billable']
        except:
            noko_project_name = "N/A"
        #
        # Extract the TAGS data
        #
        if len(jline['tags']) > 0:
            for tags in range(len(jline['tags'])):
                noko_tag_id = jline['tags'][tags]['id']
                noko_tag_name = jline['tags'][tags]['name'].upper()
                noko_tag_billable = jline['tags'][tags]['billable']
                noko_tag_formatted = jline['tags'][tags]['formatted_name'].upper()
                # Strip the tag from the description
                print(noko_desc)
                noko_desc = noko_desc.replace(noko_tag_formatted,"")
                print(noko_desc)
                #
                # Insert the tag record if it does not exist
                #
                pg_noko_sql.insert_noko_tags (noko_tag_id, noko_tag_name, noko_tag_formatted, noko_tag_billable)

                # Insert the noko_entries_tags intersection record
                pg_noko_sql.insert_noko_entries_tags(noko_tag_id, noko_entry_id)
        
        #
        # Insert the project record if it does not exist

        #
        pg_noko_sql.insert_noko_projects(noko_project_id, noko_project_name, noko_enabled, noko_billable)
        #
        #
        # Pass the extracted values to a module to create the insert SQL string
        #
        noko_desc = noko_desc.strip()
        pg_noko_sql.insert_noko_entries(noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc)

        
