#!/usr/bin/python
"""
This is the main api flask app.
It connects to the memcache (memcache must me running) and get the data.
Parses the data fetched from memcache and then displays as json format.
"""
from flask import Flask, jsonify
import memcache
import os
import logging

app = Flask(__name__)

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
        os.system('su - ec2-user "/opt/boto_get_albums.py"')

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
        os.system('su - ec2-user -c "/opt/boto_get_albums.py"')

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


if __name__ == '__main__':
    app.run(port=8080, host='0.0.0.0', debug=True)
