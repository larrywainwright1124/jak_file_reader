from db import DB
from datetime import datetime
from decimal import Decimal

db = DB('walgreens', 'root', 'root')
# result = db.proc('adjustment', (1, 100.00, 1, 'tp_trans', '--'))
# print result
# print result[4]

# data = {
#     'trans_type': '520',
#     'account_nbr': '1234567890123456',
#     'trans_date': datetime.now(),
#     'in_ts': datetime.now(),
#     'merch_name': 'fake_name',
#     'merch_city': 'fake city',
#     'merch_state': 'UT',
#     'acq_id': '12345',
#     'amt': Decimal(int('12345') / 100.0),
#     'status': 'N'
# }
# id = db.insert('tp_trans', data)
# print id