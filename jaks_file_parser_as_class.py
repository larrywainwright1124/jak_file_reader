"""
Load Modules later when I add the functions that format the data

    Create functions to read whole file and put into dictionaries inside an array. Test pulling data out of dictionaries
    List out all dictionaries
    - Will need to create subclass to read 100 characters, and parse out accordingly into dictionaries to be put into database
    - Will need to add functions to format outputted data (will need to define "type" key in the dictionary that will add formatting based on type)
    - Not sure if I have
"""


class JaksFileParserAsClass:
    def __init__(self):
        self.f = open('thefile.txt', 'r')

        self.read_header()
        self.read_record()

    def read_header(self):
        header = [
            {'identifier': 'total_records', 'data': int(self.f.read(6))},
            {'identifier': 'total_debits', 'data': int(self.f.read(6))},
            {'identifier': 'total_payments', 'data': int(self.f.read(6))},
            {'identifier': 'total_debit_amt', 'data': int(self.f.read(12))},
            {'identifier': 'total_payment_amt', 'data': int(self.f.read(12))}
        ]
        for item in header:
            print item

    def read_record(self):
        record = [
            {'identifier': 'index', 'data': int(self.f.read(6))},
            {'identifier': 'tran_type', 'data': int(self.f.read(3))},
            {'identifier': 'acc_number', 'data': int(self.f.read(16))},
            {'identifier': 'tran_date', 'data': int(self.f.read(8))},
            {'identifier': 'merchant_name', 'data': self.f.read(25)},
            {'identifier': 'city', 'data': self.f.read(23)},
            {'identifier': 'state', 'data': self.f.read(10)},
            {'identifier': 'acquire_id', 'data': int(self.f.read(5))},
            {'identifier': 'tran_amount', 'data': int(self.f.read(12))}
        ]
        for item in record:
            print item


