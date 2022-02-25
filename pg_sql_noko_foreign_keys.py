#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# Stores SQL statements for the Table: noko_entries
# ---------------------------------------------------------------------------
""" Creates/formats SQL statements for the PostgreSQL database """
import sys
from datetime import datetime
import config


idx_noko_projects_project_name =("CREATE UNIQUE INDEX idx_noko_projects_project_name ON "
    + config.schema + ".noko_projects ( noko_project_name );")

idx_noko_entries_noko_date = ("CREATE INDEX idx_noko_entries_noko_date ON "
    + config.schema + ".noko_entries ( noko_date );")

fk_noko_entries_noko_projects = ("ALTER TABLE "+config.schema
    +".noko_entries ADD CONSTRAINT fk_noko_entries_noko_projects FOREIGN KEY ( noko_project_name )"
    +" REFERENCES noko.noko_projects( noko_project_name ) ON DELETE CASCADE ON UPDATE CASCADE;")

fk_noko_entries_noko_dates = ("ALTER TABLE " + config.schema
    +".noko_entries ADD CONSTRAINT fk_noko_entries_noko_dates FOREIGN KEY ( noko_date )"
    +" REFERENCES noko.noko_dates( noko_date ) ON DELETE CASCADE ON UPDATE CASCADE;")

fk_noko_entries_tags = ("ALTER TABLE "+config.schema
    +".noko_entries_tags ADD CONSTRAINT fk_noko_entries_tags FOREIGN KEY ( noko_entry_id )"
    +" REFERENCES noko.noko_entries( noko_entry_id ) ON DELETE CASCADE ON UPDATE CASCADE;")

fk_noko_entries_tags_noko_tags =("ALTER TABLE "+ config.schema
    +".noko_entries_tags ADD CONSTRAINT fk_noko_entries_tags_noko_tags FOREIGN KEY ( noko_tag_id )"
    +" REFERENCES noko.noko_tags( noko_tag_id ) ON DELETE CASCADE ON UPDATE CASCADE;")
