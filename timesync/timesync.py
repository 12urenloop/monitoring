from flask import Flask, jsonify
import requests
import time
from threading import Thread
from config import SERVERS, REFRESH_INTERVAL



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


def get_server_sync(url):
    before = time.time()
    try:
        r = requests.get(url, timeout=1)
        server_time = r.json()['timestamp'] / 1000
    except:
        return None
    after = time.time()
    return TimeMeasurement(before, server_time, after)

def serialize(name, measurement):
        if measurement is None:
            return {'name': name, 'success': False, 'offset': 0, 'accuracy': 0}
        else:
            return {'name': name, 'success': True, 'offset': measurement.offset(), 'accuracy': measurement.accuracy()}


server_status = {}

def fetch_routine():
    while True:
        for name, url in SERVERS.items():
            server_status[name] = get_server_sync(url)
        time.sleep(REFRESH_INTERVAL / len(SERVERS))


app = Flask(__name__)


@app.route('/')
def root():
    return jsonify([serialize(name, measurement)
        for name, measurement
        in server_status.items()
    ])

if __name__ == '__main__':
    Thread(target=fetch_routine, daemon=True).start()
    app.run(debug=False, host='0.0.0.0', port=8080)
