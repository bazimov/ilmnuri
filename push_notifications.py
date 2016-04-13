#!/usr/bin/python

from gcm import *
import sqlite3
import sys

database = '/usr/share/nginx/html/api/app/tokens.db'
gcm = GCM("AIza.....")
data = {'message': '{0}'.format(sys.argv[1])}

conn = sqlite3.connect(database)
c = conn.cursor()
c.execute('select * from token_table')
all_rows = c.fetchall()
expired_list = []

for tokens in all_rows:
    reg_id = tokens[1]
    try:
        gcm.plaintext_request(registration_id=reg_id, data=data)
    except Exception as e:
        c.execute('DELETE FROM token_table WHERE data=?', (reg_id,))
        conn.commit()
        expired_list.append(reg_id)
        print e

print expired_list
