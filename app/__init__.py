#!/usr/bin/python
from flask import Flask, jsonify
import memcache
import os

app = Flask(__name__)
client = memcache.Client([('127.0.0.1', 11211)])
dictionary = client.get('album')


@app.route('/api/v1.0/albums/', methods=['GET'])
def get_tasks():
    albums = []

    if not dictionary:
        os.system('/opt/boto_get_albums.py')

    for key, value in dictionary.items():
        i = 1
        for k, v in value.items():
            output = {
                'id': i,
                'category': key,
                'album': k,
                'items': v
            }
            albums.append(output)
            i += 1

    return jsonify({'albums': albums})


@app.route('/api/v1.0/albums/<teacher>/', methods=['GET'])
def get_teacher(teacher):
    albums = []

    if not dictionary:
        os.system('/opt/boto_get_albums.py')

    for key, value in dictionary.items():
        if key == teacher:
            i = 1
            for k, v in value.items():
                output = {
                    'id': i,
                    'category': key,
                    'album': k,
                    'items': v
                }
                albums.append(output)
                i += 1

    return jsonify({'albums': albums})


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
