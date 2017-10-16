from db import DB

db = DB('walgreens', 'root', 'root')
result = db.proc('adjustment', (1, 100.00, 1, 'tp_trans', '--'))
print result
print result[4]
