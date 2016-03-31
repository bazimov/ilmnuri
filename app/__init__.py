#!/usr/bin/python
"""
This is the main api flask app.
It connects to the memcache (memcache must me running) and get the data.
Parses the data fetched from memcache and then displays as json format.
"""
from flask import Flask, jsonify, request
import memcache
import os
import logging
import sqlite3

app = Flask(__name__)

DATABASE = 'tokens.db'

def insert_token(argument):
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO token_table (data) VALUES (?)", (argument,))
    con.commit()
    con.close()

log_dir = '/var/log/apiilmnuri/'

try:
    if not os.path.exists('/var/log/apiilmnuri'):
        os.makedirs('/var/log/apiilmnuri')
except OSError:
    log_dir = '/tmp/'

logging.basicConfig(filename='{0}apilogs.log'.format(log_dir),
                    format='%(asctime)s  %(funcName)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

log = logging.getLogger(__name__)


@app.route('/')
def index():
    log.info('index page rendered.')
    return '<h1>Please use full <a href="http://api.azimov.xyz/api/v1.0/' \
           'albums/">url</a></h1>'


@app.route('/api/v1.0/albums/', methods=['GET'])
def get_tasks():
    client = memcache.Client([('127.0.0.1', 11211)])
    log.debug('connecting to memcache.')
    dictionary = client.get('album')
    albums = []

    if not dictionary:
        log.error('Dictionary empty, executing the script.')
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
    log.info('Rendering the main albums page.')
    return jsonify({'albums': sorted(albums)})


@app.route('/api/v1.0/albums/<teacher>/', methods=['GET'])
def get_teacher(teacher):
    client = memcache.Client([('127.0.0.1', 11211)])
    log.debug('connecting to memcache.')
    dictionary = client.get('album')
    albums = []

    if not dictionary:
        log.error('Dictionary empty, executing the script.')
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

    log.info('Rendering the category {0} page.'.format(teacher))
    return jsonify({'albums': sorted(albums)})


@app.route('/api/ios/albums/<teacher>/', methods=['GET'])
def ios_teacher(teacher):
    client = memcache.Client([('127.0.0.1', 11211)])
    log.debug('connecting to memcache.')
    dictionary = client.get('album')
    albums = []

    for key, value in dictionary.items():
        if key == teacher:
            i = 1
            for k, v in value.items():
                output = {
                    'id': i,
                    'category': key,
                    'album': k,
                    'items': [{'name': x, 
                               'url': 'http://dfh59cyusxnu7.cloudfront.net/{0}/'
                                      '{1}/{2}'.format(key, k, x)} for x in v]
                }
                albums.append(output)
                i += 1

    log.info('Rendering the category {0} page on ios.'.format(teacher))
    return jsonify({'albums': sorted(albums)})


@app.route('/tokens/<uuid>', methods=['POST'])
def token(uuid):
    token_id = request.json
    insert_token(token_id['data'])
    return jsonify({'uuid': uuid})


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
