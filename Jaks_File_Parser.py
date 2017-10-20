"""
Load Modules later when I add the functions that format the data

    Create functions to read whole file and put into dictionaries inside an array. Test pulling data out of dictionaries
    List out all dictionaries
    - Will need to create subclass to read 100 characters, and parse out accordingly into dictionaries to be put into database
    - Will need to add functions to format outputted data (will need to define "type" key in the dictionary that will add formatting based on type)
    - Not sure if I have
"""

f = open('thefile.txt', 'r')


def read_header():
    header = [
        {'identifier': 'total_records', 'data': int(f.read(6))},
        {'identifier': 'total_debits', 'data': int(f.read(6))},
        {'identifier': 'total_payments', 'data': int(f.read(6))},
        {'identifier': 'total_debit_amt', 'data': int(f.read(12))},
        {'identifier': 'total_payment_amt', 'data': int(f.read(12))}
    ]
    for item in header:
        print item


def read_record():
    record = [
        {'identifier': 'index', 'data': int(f.read(6))},
        {'identifier': 'tran_type', 'data': int(f.read(3))},
        {'identifier': 'acc_number', 'data': int(f.read(16))},
        {'identifier': 'tran_date', 'data': int(f.read(8))},
        {'identifier': 'merchant_name', 'data': f.read(25)},
        {'identifier': 'city', 'data': f.read(23)},
        {'identifier': 'state', 'data': f.read(10)},
        {'identifier': 'acquire_id', 'data': int(f.read(5))},
        {'identifier': 'tran_amount', 'data': int(f.read(12))}
    ]
    for item in record:
        print item


read_header()
read_record()
