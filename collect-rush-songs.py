from urllib2 import urlopen
from json import load, dump

BASE_URL = 'http://lyrics.wikia.com/api.php?artist=Rush&fmt=json'

data = load(urlopen(BASE_URL))
songs = []

for a in data['albums']:
    songs += a['songs']

songs = dict(zip(songs, [0]*len(songs))).keys()
songs.sort()

dump(songs, open('songs.json', 'w'))
