#!/usr/bin/python

from gcm import *
import sqlite3
import sys

database = '/usr/share/nginx/html/api/app/tokens.db'
gcm = GCM("Api key from google")
data = {'message': '{0}'.format(sys.argv[1])}

conn = sqlite3.connect(database)
c = conn.cursor()
c.execute('select * from token_table')
all_rows = c.fetchall()

for tokens in all_rows:
    reg_id = tokens[1]
    gcm.plaintext_request(registration_id=reg_id, data=data)
