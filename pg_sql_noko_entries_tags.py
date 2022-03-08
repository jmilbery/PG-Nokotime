#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Stores SQL statements for the Table: noko_entries_tags
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the noko_entries_tags table """
import sys
from datetime import datetime
import config

#
# Table : noko_entries_tags
#
drop_noko_entries_tags = "drop table if exists " + config.schema + ".noko_entries_tags"
#
create_noko_entries_tags = "CREATE TABLE " + config.schema + """.noko_entries_tags
    (noko_tag_id          bigint  NOT NULL  ,
	noko_entry_id        bigint  NOT NULL  ,
	load_date            date    ,
	CONSTRAINT noko_entries_tags_pkey PRIMARY KEY ( noko_tag_id, noko_entry_id ));"""
#
truncate_noko_entries_tags = "truncate table " + config.schema + ".noko_entries_tags cascade"
#
insert_noko_entries_tags = ("insert into "
    + config.schema
    + ".noko_entries_tags (noko_tag_id, noko_entry_id, load_date)"
    + " values (%s, %s, %s) on conflict do nothing")
#
# End of table
#
