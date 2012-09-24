#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: David Jelic <djelic@buksna.net>

# Fetching, parsing and synchronizing user's loved tracks from Last.fm.
# For now, it only prints loved tracks

import sys
import urllib2
import logging
from xml.dom import minidom


logging.basicConfig(filename='log.log', level=logging.DEBUG)


def get_from_lastfm(username):
    url = "http://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=%s&limit=50&api_key=b25b959554ed76058ac220b7b2e0a026" % username
    wf = urllib2.urlopen(url)
    return wf.read()


def get_from_file(username):
    filename = "%s-loved.xml" % username
    try:
        f = open(filename, 'r')
    except Exception:
        logging.warning('Failed to open %s!' % filename)
        raise
    return f.read()


def parse(username):
    logging.info("Parsing...")

    try:
        xml = get_from_file(username)
    except Exception:
        xml = get_from_lastfm(username)

    xmldoc = minidom.parseString(xml)
    lovedtracks = xmldoc.firstChild.childNodes[1]
    ttracks = int(lovedtracks.getAttribute("total"))

    for i in range(1, ttracks, 2):
        track = lovedtracks.childNodes[i].childNodes[1].childNodes[0].nodeValue
        artist = lovedtracks.childNodes[i].childNodes[9].childNodes[1].childNodes[0].nodeValue
        print (artist + " - " + track)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s username" % sys.argv[0]
        sys.exit()

    username = sys.argv[1]
    parse(username)
