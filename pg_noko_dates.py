#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-25
# Generates a set of date records for Noko Tables 
# ---------------------------------------------------------------------------
""" Generates a set of date records for Noko Tables """

from datetime import timedelta
from datetime import date
from datetime import datetime
import config
import pg_noko_sql


def generate_dates():

    start = datetime.strptime(config.start_date, "%Y-%m-%d")
    end =   datetime.strptime(config.end_date, "%Y-%m-%d")
    # get the difference between wo dates as timedelta object
    diff = end.date() - start.date()

    for date_num in range(diff.days+1):
        new_date = start + timedelta(days=date_num)
        noko_date = new_date.strftime("%Y-%m-%d")
        noko_day_of_week = new_date.strftime("%a").upper()
        noko_week_of_year = new_date.strftime("%W")
        noko_month = new_date.strftime("%-m")
        noko_year = new_date.strftime("%Y")
        noko_day_of_month = new_date.strftime("%-d")
        noko_day_of_year = new_date.strftime("%-j")
        if int(noko_month) <4:
            noko_quarter = 'Q1'
        elif int(noko_month) >3 and int(noko_month) <7:
            noko_quarter = 'Q2'
        elif int(noko_month) >6 and int(noko_month) <10:
            noko_quarter = 'Q3'
        else:
            noko_quarter = 'Q4'

        pg_noko_sql.insert_noko_dates(noko_date, noko_day_of_week, noko_week_of_year, noko_month, noko_year, noko_day_of_month, noko_day_of_year, noko_quarter)

