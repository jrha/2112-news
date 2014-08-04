from alchemyapi.alchemyapi import AlchemyAPI
from json import load, dumps
from collections import Counter
from sys import stdout, exit
import feedparser

RSS_URL = 'http://feeds.bbci.co.uk/news/technology/rss.xml'
#RSS_URL = 'http://feeds.bbci.co.uk/news/science_and_environment/rss.xml'

keywords = load(open('keywords.json'))

d = feedparser.parse(RSS_URL)

alchemyapi = AlchemyAPI()

songs = Counter()

print '  Analysing: %s ' % (d['feed']['subtitle'])
count = len(d['entries'])
i = 0.0

stdout.write('    Working:   0%')
for t in d['entries']:
    i += 1
    title = t['title']
    url = t['link']

    if 'VIDEO:' not in title and 'AUDIO:' not in title:
        response = alchemyapi.keywords('url', url)

        if response['status'] != 'ERROR':
            for w in response['keywords']:

                w = w['text']
                if w in keywords and w != 'page':
                    for s in keywords[w]:
                        songs[s] += 1
        else:
            print "\n%s: %s" % (response['status'], response['statusInfo'])
            exit(1)

    stdout.write('\b'*4 + '%3d%%' % ((i / count) * 100))
    stdout.flush()

stdout.write('\b'*4 + 'Done!\n')

print

for name, rank in songs.most_common(5):
    print '%24s %s' % (name, '='*rank)

print

lyrics = load(open('lyrics.json'))

print lyrics[songs.most_common(1)[0][0]]
