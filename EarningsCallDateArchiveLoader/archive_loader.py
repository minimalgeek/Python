import csv
import os
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime
import logging

LOG_FILENAME = 'archive_loader.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

relative_root = './DatesArchive/'

def read_files():
    ret_dict = {}
    for filename in os.listdir(relative_root):
        with open(relative_root + filename, 'r') as file:
            reader = csv.reader(file)
            dates = list(reader)
            ret_dict[filename[:-4]] = dates[2:]
    return ret_dict

def get_collection():
    db = MongoClient('localhost', 27017).python_import
    return db.zacks_earning_call_dates_archive

if __name__ == "__main__":
    report_date_dict = read_files()
    zecda = get_collection()
    for key, value in report_date_dict.items():
        previous_report_date = None
        for v in value:
            try:
                date_str = v[0].split('/')
                report_date = datetime(int(date_str[2]), int(date_str[0]), int(date_str[1]))
                ami_report_date = (report_date.year - 1900)*10000 + report_date.month*100 + report_date.day
                zecda.insert_one({
                    'ticker':key,
                    'nextReportDate':report_date,
                    'amiNextReportDate':ami_report_date,
                    'previousReportDate':previous_report_date
                })
                previous_report_date = report_date
            except Exception:
                logging.error('error happened on: ' + key + ' - ' + str(v))
