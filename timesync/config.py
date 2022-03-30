REFRESH_INTERVAL = 5

# Dictionary of (name, url)
# Expects url's to return a json dictionary containing a `time` key
#  with the amount of milliseconds since the Unix epoch
SERVERS = {
    'ronny01': 'http://172.19.0.9:8000/time',
    'ronny02': 'http://172.19.0.2:8000/time',
    'ronny03': 'http://172.19.0.3:8000/time',
    'ronny04': 'http://172.19.0.4:8000/time',
    'ronny05': 'http://172.19.0.5:8000/time',
    'ronny06': 'http://172.19.0.6:8000/time',
}
