#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Stores SQL statements for the Table: noko_tags
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the noko_tags table """
import sys
from datetime import datetime
import config

#
# Table : noko_tags
#
drop_noko_dates = "drop table if exists "+ config.schema+ ".noko_dates cascade"
#
create_noko_dates = "CREATE TABLE " + config.schema + """.noko_dates
    (noko_date            date  NOT NULL  ,
	noko_day_of_week     char(3)    ,
	noko_week_of_year    smallint    ,
	noko_month           integer    ,
	noko_year            integer    ,
	noko_day_of_month    integer    ,
	noko_day_of_year     smallint    ,
	noko_quarter         char(2)    ,
	load_date            date    ,
	CONSTRAINT noko_dates_pkey PRIMARY KEY ( noko_date )
    );"""
#
truncate_noko_dates = "truncate table " + config.schema + ".noko_dates cascade"
#
insert_noko_dates = ("insert into " 
        + config.schema
        + ".noko_dates (noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter, load_date)"
        + " values (%s, %s, %s, %s, %s, %s, %s, %s, %s);")
#
# End of table
#
