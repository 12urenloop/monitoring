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
            r =  {'name': name, 'success': False, 'offset': 0, 'accuracy': 0}
        else:
            r =  {'name': name, 'success': True, 'offset': measurement.offset(), 'accuracy': measurement.accuracy()}
        r['abs_offset'] = abs(r['offset'])
        r['abs_accuracy'] = abs(r['accuracy'])
        return r

@dataclass
class BatonStatus:
    last_seen: float = 0
    battery: float = 0
    uptime: float = 0
    rebooted: bool = False
    last_detected_at_station: str = ""


def serialize_batonstatus(mac, baton_status: BatonStatus, name: str):
    return {
        'mac': mac,
        'battery': baton_status.battery,
        'uptime': str(datetime.timedelta(seconds=baton_status.uptime / 1000)),
        'rebooted': baton_status.rebooted,
        'time_since_seen': time.time() - baton_status.last_seen,
        'name': name,
        'last_detected_at_station': baton_status.last_detected_at_station
    }

server_status = {}
station_urls = {}

# mac to baton_status
baton_status_dict = {}

per_station_last_id = {}
baton_name_to_mac = {}
baton_mac_to_name = {}
baton_mac_to_id = {}
assigned_baton_ids = set()

def first_initialize_stations():
    for name, url in station_urls.items():
        try:
            d = requests.get(url + '/last_detection', timeout=1).json()
            per_station_last_id[name] = d['detection']['id']
            logging.info(f"First init {name} now at {per_station_last_id[name]}")
        except requests.exceptions.Timeout:
            logging.info(f"Failed first init {name} (timeout)")
        except:
            logging.error(traceback.format_exc())
            logging.error(f"Failed first init {name}")

        

def update_from_station(station_name, url):
    try:
        detections = requests.get(url + f'/detections/{per_station_last_id.get(station_name, 0)}', timeout=1).json()['detections']
        begin = per_station_last_id.get(station_name, 0)
        for detection in detections:
            mac = detection['mac']
            uptime = detection['uptime_ms']
            detection_time = detection['detection_timestamp']
            battery = detection['battery']
            if mac not in baton_status_dict:
                baton_status_dict[mac] = BatonStatus(0)
            baton_status = baton_status_dict[mac]
            
            if baton_status.last_seen < detection_time and detection_time > server_start_moment:
                if uptime < baton_status.uptime - 3000:
                    baton_status.rebooted = True
                baton_status.last_seen = detection_time
                baton_status.battery = battery
                baton_status.uptime = uptime
                baton_status.last_detected_at_station = station_name
            per_station_last_id[station_name] = max(detection['id'], per_station_last_id.get(station_name, 0))
        logging.info(f"Success station update {station_name} got {per_station_last_id.get(station_name, 0) - begin} records, now at {per_station_last_id.get(station_name, 0)}")
    except requests.exceptions.Timeout:
        logging.warning(f"Failed station update {station_name} (timeout)")
    except:
        logging.error(f"Failed station update {station_name}")
        logging.error(traceback.format_exc())


def fetch_routine():
    first_initialized = False
    while True:
        logging.info(f"Will refresh every {REFRESH_INTERVAL} s")
 
        # Fetch station data from telraam
        try:
            data = requests.get(TELRAAM_STATION_URL + '/station', timeout=1).json()
            if 'name' in data[0]:
                station_urls.clear()
                for station_obj in data:
                    station_urls[station_obj['name']] = station_obj['url']
                logging.info("Telraam fetch stations success")
        except:
            logging.error("Telraam fetch stations failed")
        
        # Fetch baton data from telraam
        try:
            data = requests.get(TELRAAM_STATION_URL + '/baton', timeout=1).json()
            if 'name' in data[0]:
                baton_mac_to_name.clear()
                baton_name_to_mac.clear()
                baton_mac_to_id.clear()
                for baton_obj in data:
                    mac = baton_obj['mac'].lower()
                    name = baton_obj['name']
                    id_ = baton_obj['id']
                    baton_mac_to_name[mac] = name
                    baton_mac_to_id[mac] = id_
                    baton_name_to_mac[name] = mac
                    if mac not in baton_status_dict:
                        baton_status_dict[mac] = BatonStatus()
                logging.info("Telraam fetch batons success")
        except:
            logging.error("Telraam fetch batons failed")
        
        # Fetch team data from telraam
        try:
            data = requests.get(TELRAAM_STATION_URL + '/team', timeout=1).json()
            if 'name' in data[0]:
                assigned_baton_ids.clear()
                for team_obj in data:
                    assigned_baton_ids.add(team_obj['batonId'])
                logging.info("Telraam fetch teams success")
        except:
            logging.error("Telraam fetch teams failed")

        # # FETCH TIMESYNC
        logging.info("Starting timestamp fetch routine")
        for name, url in station_urls.items() :
            server_status[name] = get_server_sync(name, url)
        for name, url in EXTRA_SERVERS.items() :
            server_status[name] = get_server_sync(name, url)
        


        # FETCH BATON STATUS
        if not first_initialized:
            first_initialize_stations()
            first_initialized = True

        for name, url in station_urls.items() :
            update_from_station(name, url)
            logging.info(f"Fetched stations {name}")
        time.sleep(REFRESH_INTERVAL)


root = Blueprint('root', __name__, url_prefix='')

@root.route('/')
def home():
    return jsonify([
        serialize_timemeasurement(name, measurement)
        for name, measurement
        in server_status.items()
    ])

@root.route('/batons')
def batons():
    do_filter_assigned = 'filter_assigned' in request.args
    return jsonify(sorted([
        serialize_batonstatus(mac, batonstatus, baton_mac_to_name[mac])
        for mac, batonstatus
        in baton_status_dict.items()
        if (not do_filter_assigned) or (mac in baton_mac_to_id and baton_mac_to_id[mac] in assigned_baton_ids)
    ], key=lambda x: x['name']))


# --------------------------------------------------
# ---------------- LAP INSIGHT ---------------------

import requests
from pprint import pprint


@root.route('/team-lap-times', methods=['GET'])
def lap_frequencies():
    LAP_SOURCE = 3

    laps = requests.get(TELRAAM_STATION_URL + "/lap").json()
    teams = requests.get(TELRAAM_STATION_URL + "/team").json()
    teams = {t["id"]: t for t in teams}
    laps.sort(key=lambda x: x["timestamp"])

    previous_laps = {}
    team_times = {}

    data = {}

    for lap in laps:
        if lap["lapSourceId"] != LAP_SOURCE:
            continue
        team_id = lap["teamId"]
        if team_id not in team_times:
            team_times[team_id] = []
        if team_id not in previous_laps:
            previous_laps[team_id] = lap
            continue
        previous_lap = previous_laps[team_id]
        previous_laps[team_id] = lap

        team_times[team_id].append({"lap_time": (lap["timestamp"] - previous_lap["timestamp"]) /
                                                1000,
                                    "timestamp": lap["timestamp"],
                                    "team_id": team_id,
                                    "team_name": teams[team_id]["name"]})

        # if lap["timestamp"] not in data:
        #     data[lap["timestamp"]] = {}
        # data[lap["timestamp"]][team_id] = (lap["timestamp"] - previous_lap["timestamp"]) / 1000

    return team_times
    # return data

    # {hilok: [{lap-time: "", timestamp: ""}],
    #  vtk  : [{}, {}, {}]}

    # for i in sorted(team_times.keys()):
    #
    # for i in [1, 2, 22, 7]:
    #     print(f"Team {i}")
    #     for lap in team_times[i]:
    #         if lap < 30 or lap > 70:
    #             print(lap)


# --------------------------------------------------

@root.route('/reset_rebooted/<mac>', methods=['POST'])
def reset_rebooted(mac):
    if mac not in baton_status_dict:
        return 'mac address not found'
    if not baton_status_dict[mac].rebooted:
        return 'This baton was not rebooted; no need to reset it'
    baton_status_dict[mac].rebooted = False
    return 'OK'

def create_app():
    app = Flask(__name__)
    app.register_blueprint(root)

    Thread(target=fetch_routine, daemon=True).start()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, host='0.0.0.0', port=3030)
