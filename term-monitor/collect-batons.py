"""
List all detected batons in any station
"""

import requests
from pprint import pprint
from time import sleep
from datetime import datetime, timedelta

from stations import stations
from batons import batons

baton_info = {}


def get_baton_letter(mac: str):
    return batons[mac]

def fetch_detections(station, count_thousand: int = 1):
    last_detection = requests.get(f"http://{station}:8000/last_detection").json()
    last_id = last_detection["detection"]["id"]

    detections = []
    for i in range(1, count_thousand+1):
        batch_id = last_id - (i * 1000)
        detections += requests.get(f"http://{station}:8000/detections/{batch_id}").json()[
            "detections"
        ]
    return detections


for station in stations:
    try:
        detections = fetch_detections(station, 1)
    except:
        print("AAAhhhhh")
        exit(1)
    for detection in detections:
        mac = detection["mac"][-2:].upper()
        utc_dt = datetime.utcfromtimestamp(detection["detection_timestamp"])

        # Battery can drop while pulling out the power. Keep the last sensible value
        if mac in baton_info and abs(baton_info[mac]["battery"] - (detection["battery"]) > 20):
            detection["battery"] = baton_info[mac]["battery"]
        baton_info[mac] = {
            "time": utc_dt,
            "battery": detection["battery"],
            "mac": detection["mac"],
        }

RED = "\033[0;31m"
NC = "\033[0m"  # No Color

print(f"Total count: {len(baton_info)}")
print()

print("Suffix   Baton Mac             Last seen time          Battery   Letter")
print("------   ---------             --------------          -------   ------")
for suffix in batons:
    letter = get_baton_letter(suffix)
    if suffix in baton_info:
        info = baton_info[suffix]
        color = ""
        if info["time"] < (datetime.utcnow() - timedelta(minutes=3)):
            color = RED
        print(color, end="")
        print(
            "{}       {}     {}     {}   {}".format(
                suffix,
                info["mac"],
                info["time"].strftime("%m/%d/%Y, %H:%M:%S"),
                "{:5} %".format(info["battery"]),
                letter,
            ),
            end="",
        )
        print(NC)
    else:
        print("{}".format(suffix))
