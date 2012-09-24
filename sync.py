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


def get_loved_page(page=1):
    """Fetch single page of loved tracks"""

    params = {
        'method': 'user.getlovedtracks',
        'user': USERNAME,
        'limit': 50,
        'page': page,
        'api_key': API_KEY,
        'format': 'json',
    }
    url = AUDIOSCROBBLER_URL + '?' + urlencode(params)
    try:
        loved = json.load(urllib2.urlopen(url))
    except Exception:
        raise Exception('Request error occoured')

    if 'error' in loved.keys():
        raise Exception(loved['message'])

    return loved['lovedtracks']


def get_loved_tracks():
    """Iterate over total number of pages and return dictionary
    of artists and tracks. Array of loved tracks belongs to each artist.
    """

    pages = int(get_loved_page()['@attr']['totalPages'])
    loved_parsed = {}

    for pagenum in xrange(1, pages):
        sys.stdout.write("Parsing page: %d/%d\r" % (pagenum, pages))
        sys.stdout.flush()
        # fetch page of loved tracks
        loved = get_loved_page(pagenum)

        for track in loved['track']:
            title = track['name']
            artist = track['artist']['name']
            if not artist in loved_parsed.keys():
                loved_parsed[artist] = [title]
            else:
                loved_parsed[artist].append(title)

        sleep(SLEEP_SEC)

    return loved_parsed


if __name__ == '__main__':
    sys.stdout.write('Starting...\n')
    # retrieve loved tracks from Last.fm service and save locally
    json.dump(get_loved_tracks(), open('dump.json', 'w'))
    # retrieve from backup
    pprint(_inflate_from_file('dump.json'))
