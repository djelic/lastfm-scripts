Last.fm Scripts
======================

A set of Python scripts that use Last.fm as a data source created for various purposes,
mainly sync desktop music player with Last.fm.




Loved Track Sync
----------------

loved_parser.py - fetching, parsing and synchronizing user's loved tracks from Last.fm.
For now, it only prints loved tracks

### Usage

```
loved_parser.py username
```

New Album Releases
------------------

album_releases.py - notifies user when new album is released based on Last.fm music profile.
User should be able to filter artist, from whom notifications should appear,by number of plays already played from that artist.

### Usage

Edit script and set folowing constants:

* API_KEY - You don't need to change this, default API key should work
* USERNAME - Your Last.fm username
* MIN_PLAYS - Minimum number of tracks that the user has listened to by a particular artist. Only albums from artists with greater number of plays than MIN_PLAYS will be displayed.