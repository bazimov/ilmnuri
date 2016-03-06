#!/usr/bin/python
from flask import Flask, jsonify
import memcache
import os

app = Flask(__name__)
client = memcache.Client([('127.0.0.1', 11211)])
albums = []

dictionary = client.get('album')

if not dictionary:
    os.system('/opt/boto_get_albums.py')

for key, value in dictionary.items():
    for k, v in value.items():
        output = {
            'category': key,
            'album': k,
            'items': v
        }
        albums.append(output)


@app.route('/api/v1.0/albums', methods=['GET'])
def get_tasks():
    return jsonify({'albums': albums})

if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
