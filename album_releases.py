#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: David Jelic <djelic@buksna.net>

# Notifies user when new album is released based on Last.fm music profile.
# User should be able to filter artist, from whom notifications should appear,
# by number of plays already played from that artist.


from urllib import urlencode
from urllib2 import urlopen
import json


API_KEY = 'b25b959554ed76058ac220b7b2e0a026'
USERNAME = 'burgulgoth'
MIN_PLAYS = 200


def get_artist_playcount(artist):
    params = {
        'method': 'user.getartisttracks',
        'user': USERNAME,
        'artist': artist,
        'api_key': API_KEY,
        'format': 'json',
    }
    ARTIST_TRACKS_URL = "http://ws.audioscrobbler.com/2.0/?%s" % urlencode(params)

    tracks = json.load(urlopen(ARTIST_TRACKS_URL))
    if 'error' in tracks.keys():
        print "Error no.: %s occoured: %s\n" % (tracks['error'],
            tracks['message'])
        return None

    try:
        total_plays = int(tracks['artisttracks']['@attr']['total'])
    except Exception:
        return None

    return total_plays


def main():
    params = {
        'method': 'user.getnewreleases',
        'user': USERNAME,
        'api_key': API_KEY,
        'format': 'json',
    }
    NEW_RELEASES_URL = "http://ws.audioscrobbler.com/2.0/?%s" % urlencode(params)

    releases = json.load(urlopen(NEW_RELEASES_URL))
    if 'error' in releases.keys():
        print "Error no.: %s occoured: %s\n" % (releases['error'],
            releases['message'])
        return None

    for album in releases['albums']['album']:
        album_name = album['name']
        album_artist = album['artist']['name']
        artist_plays = get_artist_playcount(album_artist)
        if artist_plays > MIN_PLAYS:
            print u' ::: '.join((album_artist, album_name)).encode('utf-8').strip()

if __name__ == '__main__':
    main()
