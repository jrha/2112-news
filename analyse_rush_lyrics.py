from alchemyapi.alchemyapi import AlchemyAPI
from json import load, dump
import time

songs = load(open('lyrics.json'))

alchemyapi = AlchemyAPI()

keywords = {}

for song in songs:
    response = alchemyapi.keywords('text', songs[song])

    for k in [ c['text'] for c in response['keywords'] ]:
        if k not in keywords:
            keywords[k] = []
        keywords[k].append(song)

dump(keywords, open('keywords.json', 'w'))
