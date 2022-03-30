REFRESH_INTERVAL = 5

# Dictionary of (name, url)
# Expects url's to return a json dictionary containing a `time` key
#  with the amount of milliseconds since the Unix epoch
SERVERS = {
    'ronny01': 'http://localhost:8000/time',
}
