CREATE SCHEMA IF NOT EXISTS noko;

CREATE  TABLE noko.noko_dates ( 
	noko_date            date  NOT NULL  ,
	noko_day_of_week     char(3)    ,
	noko_week_of_year    smallint    ,
	noko_month           integer    ,
	noko_year            integer    ,
	noko_day_of_month    integer    ,
	noko_day_of_year     smallint    ,
	noko_quarter         char(2)    ,
	load_date            date    ,
	CONSTRAINT noko_dates_pkey PRIMARY KEY ( noko_date )
 );

CREATE  TABLE noko.noko_projects ( 
	noko_project_id      bigint  NOT NULL  ,
	noko_project_name    varchar(128)    ,
	noko_description     varchar(1024)    ,
	noko_enabled         boolean    ,
	noko_billable        boolean    ,
	load_date            date    ,
	CONSTRAINT noko_projects_pkey PRIMARY KEY ( noko_project_id )
 );

CREATE  TABLE noko.noko_tags ( 
	noko_tag_id          bigint  NOT NULL  ,
	noko_tag_name        varchar(128)    ,
	noko_tag_formatted   varchar(128)    ,
	noko_tag_billable    boolean    ,
	load_date            date    ,
	CONSTRAINT noko_tags_pkey PRIMARY KEY ( noko_tag_id )
 );

CREATE  TABLE noko.noko_entries ( 
	noko_entry_id        bigint  NOT NULL  ,
	noko_project_name    varchar(128)    ,
	noko_user            varchar(512)    ,
	noko_date            date    ,
	noko_minutes         integer    ,
	noko_desc            varchar(2048)    ,
	load_date            date    ,
	CONSTRAINT noko_entries_pkey PRIMARY KEY ( noko_entry_id ),
	CONSTRAINT idx_noko_entries_project_name UNIQUE ( noko_project_name ) 
 );

CREATE  TABLE noko.noko_entries_tags ( 
	noko_tag_id          bigint  NOT NULL  ,
	noko_entry_id        bigint  NOT NULL  ,
	load_date            date    ,
	CONSTRAINT noko_entries_tags_pkey PRIMARY KEY ( noko_tag_id, noko_entry_id )
 );

CREATE UNIQUE INDEX idx_noko_projects_project_name ON noko.noko_projects ( noko_project_name );

CREATE INDEX idx_noko_entries_noko_date ON noko.noko_entries ( noko_date );

ALTER TABLE noko.noko_entries ADD CONSTRAINT fk_noko_entries_noko_projects FOREIGN KEY ( noko_project_name ) REFERENCES noko.noko_projects( noko_project_name ) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE noko.noko_entries ADD CONSTRAINT fk_noko_entries_noko_dates FOREIGN KEY ( noko_date ) REFERENCES noko.noko_dates( noko_date ) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE noko.noko_entries_tags ADD CONSTRAINT fk_noko_entries_tags FOREIGN KEY ( noko_entry_id ) REFERENCES noko.noko_entries( noko_entry_id ) ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE noko.noko_entries_tags ADD CONSTRAINT fk_noko_entries_tags_noko_tags FOREIGN KEY ( noko_tag_id ) REFERENCES noko.noko_tags( noko_tag_id ) ON DELETE CASCADE ON UPDATE CASCADE;

