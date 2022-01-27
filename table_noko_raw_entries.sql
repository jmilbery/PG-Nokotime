/* Raw Table Entries  */
CREATE TABLE postgres.noko.noko_raw_entries (
	noko_entry_id bigint NOT NULL,
	noko_user varchar(512),
	noko_date date,
	noko_minutes integer,
	noko_desc varchar(2048),
	load_date date,
	PRIMARY KEY (noko_entry_id)
);
