import argparse
from db import DB
from datetime import datetime, date, timedelta
from decimal import Decimal
import os
import sys


class Header:
    def __init__(self):
        self.record_count = 0
        self.nbr_debits = 0
        self.nbr_payments = 0
        self.total_debits = Decimal('0.0')
        self.total_payments = Decimal('0.0')


class Record:
    def __init__(self):
        self.index = 0
        self.transaction_type = ''
        self.account_nbr = ''


class Parser:
    def __init__(self, dbname, file_name):
        self.dbname = dbname
        self.file_name = file_name
        self.db = DB(self.dbname, 'root', 'root')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage=None, description="Parse data file into tp_trans")
    parser.add_argument('dbname', help="Name of the database to work with")
    parser.add_argument('file_name', help="Full path to the file to parse")

    args = parser.parse_args()
    print args.dbname
    print args.file_name
