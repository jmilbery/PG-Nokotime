#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Stores SQL statements for the Table: noko_tags
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the PostgreSQL database """
import sys
from datetime import datetime
import config

#
# Table : noko_tags
#
drop_noko_tags = "drop table if exists "+ config.schema+ ".noko_tags cascade"
#
create_noko_tags = "CREATE TABLE "+ config.schema + """.noko_tags
    (noko_tag_id int8 NOT NULL,
    noko_tag_name varchar(128),
    noko_tag_formatted varchar(128),
    noko_tag_billable bool,
    load_date date,
    PRIMARY KEY (noko_tag_id))"""
#
truncate_noko_tags = "truncate table " + config.schema + ".noko_tags cascade"
#
insert_noko_tags =("insert into " 
        + config.schema
        + ".noko_tags (noko_tag_id, noko_tag_name,noko_tag_formatted, noko_tag_billable, load_date)"
        + " values (%s, %s, %s, %s, %s) on conflict do nothing")
#
# End of table
#
