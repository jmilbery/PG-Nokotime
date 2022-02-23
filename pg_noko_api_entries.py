#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Calls the Nokotime Entries API and processes the records
# ---------------------------------------------------------------------------
""" Formats and Calls an API call for Noko ENTRIES called by pg_noko_main """
import requests
import sys
from datetime import datetime
import pg_noko_sql
import pg_noko_logger


def get_entries(conn,api_root,per_page,noko_token):
    """ Format and call Noko ENTRIES api call with paging paramters """

    # Call the Noko Entries API with four parameters (found in the config.py file)
    #   Per_page -- maximum number of entries records per page
    #   Api_root -- Not a Noko parameter per se, it's the vanilla Entris API url
    #   Page_max -- maximum number of pages, not a Noko parameter, a small hack to limit
    #               total loops over entries (we drop out of the loop when we get
    #               a null entry response anyway)
    try:
        page = 0
        #for page in range(1,page_max):
        while True:
            page = page + 1
            #
            # Create API string from config.sys variables in the [noko] section
            #
            api_url = api_root +"entries?"+ "per_page=" + str(per_page) + "&" + "noko_token=" + noko_token + "&page="+str(page)
            response = requests.get(api_url)
            #
            # Process response, exit when the API returns a null json doc (it's a little
            # hinky in the API, so we strip blanks and look for an empty
            # JSON doc "[]")
            #
            if response.text.strip() == "[]":
                #
                # return to pg_noko_main and exit.
                return
            else:
                #
                # JSON doc is not empty, so pass the results to process_entries
                # for parsing
                #
                process_entries(conn,response)
    except Exception as e:
        exit_message = "ERROR get_entries " + str(e)
        print(response.text)
        sys.exit(exit_message)


def process_entries(conn,response):
    """ Process the JSON packet that is returned from Noko API call """
    data = response.json()
    #
    # For each JSON "record" -- extract the desired elements (take a look at the Noko API
    # docs to understand the JSON format)
    #
    # For our purposes we don't need or want all of the elements of the
    # JSON doc.  If you need more elements you can add them here -- and
    # you will need to add them to the PostgreSQL tables and pg_noko_sql as
    # well.
    for jline in data:
        # record id -- elements at the top of the hierarchy use a single
        # element index
        noko_entry_id = str(jline['id'])
        # user -- user email is below user in the hierarchy, so we need two elements
        # We also force to uppercase (we are storing everything uppercase in the DB)
        noko_user =  jline['user']['email'].upper()
        # Date
        noko_date = str(jline['date']).upper()
        # minutes
        noko_minutes = str(jline['minutes'])
        # description
        # We strip out embedded commas from the description as we don't want them.
        #
        noko_desc = jline['description'].replace(",","").upper()
        #
        # Strip out single quotes from the description to make our SQL queries easier
        # later on.
        #
        noko_desc = noko_desc.replace("'","")
        #
        # billable
        noko_billable = jline['billable']
        #
        # It's possible to have a null project, so we try to extract the name,
        # but if it fails, we force it to "N/A".  We don't want our users to
        # leave the project field blank -- but there is no way to prevent it
        #
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
            noko_project_id = 0
            noko_enabled = False
            noko_billable = False
        #
        # Extract the TAGS data -- if it exists for the entry (entries
        # are not required to have TAGS)
        #
        if len(jline['tags']) > 0:
            #
            # Tags section of the JSON doc has a non-zero length,
            # so extract the tags
            #
            for tags in range(len(jline['tags'])):
                #
                # Difference here as compared to entries is that there can be
                # multiple tags per entry, so you need the TAG record index to
                # pull the correct data
                #
                noko_tag_id = jline['tags'][tags]['id']
                noko_tag_name = jline['tags'][tags]['name'].upper()
                noko_tag_billable = jline['tags'][tags]['billable']
                noko_tag_formatted = jline['tags'][tags]['formatted_name'].upper()
                #
                # Strip the tag from the description.  Noko embeds the tags data
                # into the descriptions, which is our core problem with reporting.
                # We use the formatted tag field (it has the leading # sign) and
                # we replace it in the description string with nothing -- which
                # strips it out of the description.
                #
                noko_desc = noko_desc.replace(noko_tag_formatted,"")
                #
                # After we strip the tag from the description, we enter the tag
                # into the noko_tags table by passing the fields to the insert_noko_tags
                # method in the pg_noko_sql library.  You'll note in that code that we use
                # the "on conflict do nothing" insert qualifier, so we don't have to 
                # worry about duplicates.  Noko provides a unique TAG_ID as a primary key
                # field, and that's how we match
                #
                pg_noko_sql.insert_noko_tags (conn,noko_tag_id, noko_tag_name, noko_tag_formatted, noko_tag_billable)
                #
                # Noko_tags record is loaded, so now we insert a record in the intersection
                # table - noko_entries_tags.  This way, each NOKO_ENTRIES record will have zero
                # or more NOKO_ENTRIES_TAGS records
                #
                pg_noko_sql.insert_noko_entries_tags(conn,noko_tag_id, noko_entry_id)
        
        #
        # Now we store the project record, using the same concept as tags - use the Noko supplied
        # project_id and insert with "on conflict do nothing" SQL variant.
        #
        pg_noko_sql.insert_noko_projects(conn,noko_project_id, noko_project_name, noko_enabled, noko_billable)
        #
        #
        # Last, but not least -- load the noko_entries record itself.  This is a little sloppy,
        # as this insert could fail and we would have TAGS and PROJECTS that do not have an entry,
        # but this is not a big problem for our data
        #
        # Remove any remaining leading/trailing spaces from the description -- which can
        # happen more often because we have pulled out the TAG data from the description
        #
        noko_desc = noko_desc.strip()
        pg_noko_sql.insert_noko_entries(conn,noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc)

        
