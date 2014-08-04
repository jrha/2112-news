from json import load, dump
import lyricsScraper

songs = load(open('songs.json'))
lyrics = {}

fetcher = lyricsScraper.LyricsFetcher()

for song in songs:
    l = fetcher.get_lyrics('rush', song)
    if l:
        lyrics[song] = l.lyrics
        dump(lyrics, open('lyrics.json', 'w'))
