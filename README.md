# PG Nokotime
 Python/PostgreSQL code for importing and managing Nokotime data.

 This is a relatively simple bit of Python code to pull time
 entry data from Nokotime (nokotime.com) and load the results
 into a PostgreSQL database.

 Pg_noko.pdf shows the database schema that we are using -- it's a simple
 star schema (with very few dimensional variables -- but you can add to it
 as needed -- including appending data from outside of Noko).

 The python code creates the tables WITHOUT additional indexes or
 foreign keys -- you can modify the code, or simply run the pg_noko.sql
 script to create the tables with indexes and foreign keys.  The
 pg_noko_api_entries python code loads the records from the dimensions
 to the fact table (noko_entries/noko_entries_tags) - so it WILL
 work with foreign keys in place.

To Run the Code:

Python:

    You need psycopg2 installed:

        pip3 install psycopg2-binary

    Code has been tested with Python 3.9.7 -- should work with any
    version of python3

    Rename sample_config.py to config.py  (This is not super-secure, but it's
    fine for a single developer running from your local machine, even if the
    DB is remote).

PostgreSQL:

    You'll need a PostgreSQL database and schema, I've tested it locally
    and with AWS AuroraDB/PostgreSQL.

Nokotime:

    You will need your API key from Noko:
    
        Noko Main Screen/"Integrations & Apps"/Noko API/Personal Access Tokens/+Settings/+Create token

    Add your token to the config.py file to the noko_token variable.


