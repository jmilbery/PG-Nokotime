#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Stores SQL statements for the Table: noko_projects
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the PostgreSQL database """
import sys
from datetime import datetime
import config

#
# Table : noko_projects
#
drop_noko_projects = "drop table if exists "+ config.schema + ".noko_projects cascade"
#
create_noko_projects = "CREATE TABLE " + config.schema + """.noko_projects
    (noko_project_id      bigint  NOT NULL  ,
	noko_project_name    varchar(128)    ,
	noko_description     varchar(1024)    ,
	noko_enabled         boolean    ,
	noko_billable        boolean    ,
	load_date            date    ,
	CONSTRAINT noko_projects_pkey PRIMARY KEY ( noko_project_id ));"""
#
truncate_noko_projects = "truncate table " + config.schema + ".noko_projects cascade"
#
insert_noko_projects = ("insert into "
    + config.schema
    + ".noko_projects (noko_project_id, noko_project_name, noko_enabled, noko_billable, load_date)"
    + " values (%s, %s, %s, %s, %s) on conflict do nothing")
#
# End of table
#
