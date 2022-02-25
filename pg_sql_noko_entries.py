#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Stores SQL statements for the Table: noko_entries
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the PostgreSQL database """
import sys
from datetime import datetime
import config

#
# Table : noko_entries
#
drop_noko_entries = "drop table if exists "+ config.schema+ ".noko_entries cascade"
#
create_noko_entries = "CREATE TABLE "+ config.schema + """.noko_entries (
    noko_entry_id        bigint  NOT NULL  ,
	noko_project_name    varchar(128)    ,
	noko_user            varchar(512)    ,
	noko_date            date    ,
	noko_minutes         integer    ,
	noko_desc            varchar(2048)    ,
	load_date            date    ,
	CONSTRAINT noko_entries_pkey PRIMARY KEY ( noko_entry_id ));"""
#
truncate_noko_entries = "truncate table " + config.schema + ".noko_entries cascade"
#
insert_noko_entries = ("insert into "
    + config.schema
    + ".noko_entries (noko_entry_id, noko_project_name, noko_user, noko_date, noko_minutes, noko_desc, load_date)"
    + " values (%s, %s, %s, %s, %s, %s, %s) on conflict do nothing;")
#
# End of table
#
