from socket import timeout
from flask import Flask, jsonify, Blueprint, request
import requests
import time
from threading import Thread
from dataclasses import dataclass
from config import REFRESH_INTERVAL, TELRAAM_STATION_URL, EXTRA_SERVERS, LOGGING_LEVEL
import traceback
import datetime
import logging

logging.getLogger().setLevel(LOGGING_LEVEL)
server_start_moment = time.time()


class TimeMeasurement:
    def __init__(self, before, server_time, after):
        self.before = before
        self.server_time = server_time
        self.after = after

    def offset(self):
        '''Get difference in seconds between server and us. Will be positive if server clock is further than us'''
        middle = self.before + (self.after - self.before) / 2
        return (self.server_time - middle)

    def accuracy(self):
        return self.after - self.before


def get_server_sync(name, url):
    before = time.time()
    try:
        r = requests.get(url + '/time', timeout=1)
        server_time = r.json()['timestamp'] / 1000
        logging.info(f"Fetched timesync {name}")
    except requests.exceptions.Timeout:
        logging.warning(f"Failed timesync {name}")
        return None
    except Exception as e:
        logging.error(f"Failed timesync {name}")
        logging.error(traceback.format_exc())
        return None
    after = time.time()
    return TimeMeasurement(before, server_time, after)


def serialize_timemeasurement(name, measurement):
    if measurement is None:
        r = {'name': name, 'success': False, 'offset': 0, 'accuracy': 0}
    else:
        r = {'name': name, 'success': True, 'offset': measurement.offset(), 'accuracy': measurement.accuracy()}
    r['abs_offset'] = abs(r['offset'])
    r['abs_accuracy'] = abs(r['accuracy'])
    return r

server_status = {}
station_urls = {}

def fetch_routine():
    while True:
        logging.info(f"Will refresh every {REFRESH_INTERVAL} s")
        # # FETCH TIMESYNC
        logging.info("Starting timestamp fetch routine")
        for name, url in station_urls.items():
            server_status[name] = get_server_sync(name, url)
        for name, url in EXTRA_SERVERS.items():
            server_status[name] = get_server_sync(name, url)

        time.sleep(REFRESH_INTERVAL)


root = Blueprint('root', __name__, url_prefix='')


@root.route('/')
def home():
    return jsonify([
        serialize_timemeasurement(name, measurement)
        for name, measurement
        in server_status.items()
    ])


def create_app():
    app = Flask(__name__)
    app.register_blueprint(root)

    Thread(target=fetch_routine, daemon=True).start()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=3030)
