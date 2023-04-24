import logging

# LOGGING_LEVEL = logging.INFO
LOGGING_LEVEL = logging.INFO
REFRESH_INTERVAL = 1

TELRAAM_STATION_URL = 'http://$IP_PORT_TELRAAM'

# Dictionary of (name, url)
# Expects url's to have a `/time` endpoint returning a json dictionary containing a `time` key
#  with the amount of milliseconds since the Unix epoch
EXTRA_SERVERS = {
    'Telraam': TELRAAM_STATION_URL,
    'Manualcount': 'http://$IP_PORT_MANUALCOUNT',
}
