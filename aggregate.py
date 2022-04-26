"""
Shows an aggregate of different lap sources compared to eachother
"""

import requests
import matplotlib.pyplot as plt
import json
from pprint import pprint

TELRAAM_URL = "http://172.12.50.21:8080"

def process_laps(laps):
    counts = {}

    for lap in laps:
        if lap["timestamp"] < 1648737000000:
            continue
        teamId = lap["teamId"]
        team = teams[teamId]["name"]

        if team not in counts:
            counts[team] = {}

        lapSourceId = lap["lapSourceId"]
        lapSourceName = sources[lapSourceId]['name']
        if lapSourceName not in counts[team]:
            counts[team][lapSourceName] = 0
        counts[team][lapSourceName] += 1
    return counts



laps = requests.get("{}/lap".format(TELRAAM_URL)).json()
teams = requests.get(TELRAAM_URL + "/team").json()
sources = requests.get(TELRAAM_URL + "/lap-source").json()
laps_combi = requests.get(TELRAAM_URL + "/accepted-laps").json()

teams = { team['id']: team for team in teams }
sources = { source['id']: source for source in sources }

for lap in laps_combi:
    lap['lapSourceId'] = '10'
sources['10'] = { 'name': 'combi_lapper', 'id': '10' }

count_laps = process_laps(laps)
count_combi_laps = process_laps(laps_combi)

for k in count_laps.keys():
    count_laps[k] = {**count_laps[k], **count_combi_laps[k]}

print(json.dumps(count_laps))

#print(count_laps[list(teams.values())])
team_names = list(map(lambda a:a['name'], sorted(teams.values(), key=lambda a:count_laps.get(a['name'], dict()).get('combi_lapper', 0), reverse=True)))
manuel = [count_laps.get(d,dict()).get('manual-count', 0) for d in team_names]
viterbi = [count_laps.get(d,dict()).get('viterbi-lapper', 0) for d in team_names]
combi = [count_laps.get(d,dict()).get('combi_lapper', 0) for d in team_names]

barWidth = .25
br1 = list(range(len(team_names)))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, manuel, color ='r', width = barWidth,
        edgecolor ='grey', label ='manuel')
plt.bar(br2, viterbi, color ='g', width = barWidth,
        edgecolor ='grey', label ='viterbi')
plt.bar(br3, combi, color ='b', width = barWidth,
        edgecolor ='grey', label ='combi')

plt.xlabel('Team naam (eerste 3 letters)')
plt.ylabel('Count laps')
plt.xticks([r + barWidth for r in br1], [d[:3] for d in team_names])

plt.legend()
plt.savefig('aggregate.py.png')
