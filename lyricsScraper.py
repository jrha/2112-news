#-*- coding: UTF-8 -*-
import sys, re, urllib2, socket, HTMLParser

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

socket.setdefaulttimeout(10)

LIC_TXT = 'we are not licensed to display the full lyrics for this song at the moment'

def log(txt):
    print "INFO: "+txt

class Lyrics:
    def __init__(self):
        self.lyrics = ""
        self.source = ""
        self.list = None
        self.lrc = False

class LyricsFetcher:
    def __init__( self ):
        self.url = 'http://lyrics.wikia.com/api.php?artist=%s&song=%s&fmt=realjson'

    def get_lyrics(self, artist, title):
        log( "searching lyrics for %s - %s" % (artist, title))
        lyrics = Lyrics()

        try:
            req = urllib2.urlopen(self.url % (urllib2.quote(artist), urllib2.quote(title)))
            response = req.read()
        except:
            return None
        req.close()
        data = simplejson.loads(response)
        try:
            self.page = data['url']
        except:
            return None
        if not self.page.endswith('action=edit'):
            log( "search url: %s" % (self.page))
            try:
                req = urllib2.urlopen(self.page)
                response = req.read()
            except urllib2.HTTPError, error: # strange... sometimes lyrics are returned with a 404 error
                if error.code == 404:
                    response = error.read()
                else:
                    return None
            req.close()
            matchcode = re.search('lyricbox.*?div>(.*?)<!--', response)
            try:
                lyricscode = (matchcode.group(1))
                htmlparser = HTMLParser.HTMLParser()
                lyricstext = htmlparser.unescape(lyricscode).replace('<br />', '\n')
                lyr = re.sub('<[^<]+?>', '', lyricstext)
                if LIC_TXT in lyr:
                    return None
                lyrics.lyrics = lyr
                return lyrics
            except AttributeError:
                return None
        else:
            return None
