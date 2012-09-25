#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: David Jelic <djelic@buksna.net>

import sys
import urllib2
import json
from urllib import urlencode
from pprint import pprint
from time import sleep

USERNAME = 'burgulgoth'
API_KEY = '4b7393188fa6c24b508de8faf52a460b'

AUDIOSCROBBLER_URL = 'http://ws.audioscrobbler.com/2.0/'
SLEEP_SEC = 2


def _inflate_from_file(filename):
    """Get loved tracks from local JSON file"""

    try:
        return json.load(open(filename, 'r'))
    except Exception:
        return None


def fetch_page(method, page=1, limit=50):
    params = {
        'user': USERNAME,
        'limit': limit,
        'page': page,
        'api_key': API_KEY,
        'format': 'json',
    }
    if method == 'loved':
        params['method'] = 'user.getlovedtracks'
    elif method == 'recent':
        params['method'] = 'user.getrecenttracks'
    else:
        return

    url = AUDIOSCROBBLER_URL + '?' + urlencode(params)
    try:
        page = json.load(urllib2.urlopen(url))
    except Exception:
        raise Exception('Request error occoured')

    if 'error' in page.keys():
        raise Exception(page['message'])

    return page[page.keys()[0]]


def get_tracks(method):
    pages = int(fetch_page(method)['@attr']['totalPages'])
    tracks_parsed = {}

    for pagenum in xrange(1, pages - (pages - 4)):
        sys.stdout.write("Parsing page: %d/%d\r" % (pagenum, pages - (pages - 4)))
        sys.stdout.flush()
        # fetch page of loved tracks
        tracks = fetch_page(method, page=pagenum)

        for track in tracks['track']:
            title = track['name']
            if method == 'loved':
                artist = track['artist']['name']
                if not artist in tracks_parsed.keys():
                    tracks_parsed[artist] = [title]
                else:
                    tracks_parsed[artist].append(title)
            if method == 'recent':
                artist = track['artist']['#text']
                if not artist in tracks_parsed.keys():
                    tracks_parsed[artist] = dict()
                    tracks_parsed[artist][title] = 1
                else:
                    if not title in tracks_parsed[artist].keys():
                        tracks_parsed[artist][title] = 1
                    else:
                        tracks_parsed[artist][title] += 1

        sys.stdout.write("Sleeping for %d seconds...\r" % (SLEEP_SEC))
        sys.stdout.flush()
        sleep(SLEEP_SEC)

    return tracks_parsed


if __name__ == '__main__':
    sys.stdout.write('Starting...\n')
    # retrieve loved tracks from Last.fm service and save locally
    # json.dump(get_tracks('loved'), open('loved.json', 'w'))
    json.dump(get_tracks('recent'), open('recent.json', 'w'))
    # retrieve from backup
    # pprint(_inflate_from_file('dump.json'))
