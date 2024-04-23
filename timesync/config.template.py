import logging

# LOGGING_LEVEL = logging.INFO
LOGGING_LEVEL = logging.INFO
REFRESH_INTERVAL = 1

# Dictionary of (name, url)
# Expects url's to have a `/time` endpoint returning a json dictionary containing a `time` key
#  with the amount of milliseconds since the Unix epoch
EXTRA_SERVERS = {
    'Telraam': 'http://$IP_PORT_TELRAAM',
    'Manualcount': 'http://$IP_PORT_MANUALCOUNT',
    'Ronny-01': 'http://$IP_PORT_RONNY01',
    'Ronny-02': 'http://$IP_PORT_RONNY02',
    'Ronny-03': 'http://$IP_PORT_RONNY03',
    'Ronny-04': 'http://$IP_PORT_RONNY04',
    'Ronny-05': 'http://$IP_PORT_RONNY05',
    'Ronny-06': 'http://$IP_PORT_RONNY06',
    'Ronny-07': 'http://$IP_PORT_RONNY07',
    'Ronny-08': 'http://$IP_PORT_RONNY08',
}
