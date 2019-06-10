import datetime
import csv
import ijson
import itertools
import pylast
from models import ListenHistory, Track

access_token = None

def auth(request):
    global access_token
    if access_token:
        return access_token
    url = 'https://api.zenobase.com/oauth/token'
    params = {
        'grant_type': 'password',
        'username': request['username'],
        'password': request['password'],
    }
    response = requests.post(url, params=params)
    access_token = json.loads(response.text)['access_token']
    return access_token

def trimDurations(items):
    last = None
    for item in sorted(items, key=lambda a: a['timestamp']):
        if last is not None:
            maximumDuration = item['timestamp'] - last['timestamp']
            if last['listenDuration'] > maximumDuration:
                last['listenDuration'] = maximumDuration
            yield last
        last = item
    yield last

def mergeItems(items):
    for sequence in findSequences(items):
        item = min(sequence, key=lambda a: a['timestamp'])
        startTime = min(a['timestamp'] for a in sequence)
        endTime = max(a['timestamp'] for a in sequence)
        minPercentage = min(a['percentage'] for a in sequence)
        maxPercentage = max(a['percentage'] for a in sequence)
        listenDuration = min((endTime-startTime), (maxPercentage-minPercentage)/100*item['duration'])
        if listenDuration.total_seconds() < 20:
            listenDuration = item['duration']
            
        item['listenDuration'] = listenDuration
        yield item

def formatPhoneData(item):
    action, app, album, artist, title, duration, progress, timestamp = tuple(item)
    if app not in ('com.bambuna.podcastaddict'):
        return None
    return {
        'title': title,
        'album': album,
        'artist': artist,
        'action': action,
        'isPodcast': True,
        'timestamp': datetime.datetime.fromisoformat(timestamp),
        'duration': datetime.timedelta(seconds=int(duration)/1000),
        'percentage': float(progress)/float(duration),
    }

def formatZenobaseData(item):
    duration, title, album, artist, percentage, action, app, timestamp = tuple(item)
    if app not in ('com.bambuna.podcastaddict', 'com.spotify.music'):
        return None
    return {
        'title': title,
        'album': album,
        'artist': artist,
        'action': action,
        'isPodcast': app == 'com.bambuna.podcastaddict',
        'timestamp': datetime.datetime.fromisoformat(timestamp[:-1]),
        'duration': datetime.timedelta(seconds=int(duration)/1000),
        'percentage': float(percentage),
    }
def formatLastFmTrack(track):
    return {
        'title': track.track.title,
        'album': track.album,
        'artist': track.track.artist.name,
        'action': 'start',
        'isPodcast': False,
        'timestamp': datetime.datetime.fromtimestamp(int(track.timestamp)),
        'duration': datetime.timedelta(seconds=-1),
        'percentage': 1
    }
    
def sameTrack(track1, track2):
    if track1['title'] == track2['title']:
        return True
    if track1['isPodcast'] and track1['artist'] == track2['artist'] and track1['duration'] == track2['duration']:
        return True
    return False
    
def findSequences(items):
    items = [i for i in items if i is not None]
    if not items:
        return
    items = sorted(items, key=lambda a: a['timestamp'])
    podcasts = [i for i in items if i['isPodcast']]
    music = [i for i in items if not i['isPodcast']]
    for set in (podcasts, music):        
        currentTrack = None
        sequence = []
        for item in set:
            if currentTrack and not sameTrack(currentTrack, item):
                yield sequence
                sequence = []
            currentTrack = item
            sequence.append(item)
        if sequence:
            yield sequence
            
def callLastFm(credentials, start, end):
    network = pylast.LastFMNetwork(api_key=credentials['apikey'], api_secret=credentials['secret'])
    user = network.get_user(credentials['username'])
    tracks = user.get_recent_tracks(limit=None, time_from=start, time_to=end)
    return map(formatLastFmTrack, tracks)
    
def call(sources, start, end):
    csvfile = open(sources['zenobase'], 'r', encoding="utf8")
    items = map(formatZenobaseData, csv.reader(csvfile, delimiter=',', quotechar='"'))
    # for phoneFile in sources['phone']:
        # audiofile = open(phoneFile, 'r'):
        # items = itertools.chain(items,map(formatPhoneData, ijson.items(audiofile)))
    items = itertools.chain(items, callLastFm(sources['lastfm'], start, end))
    
    for item in trimDurations(mergeItems(items)):
        track = Track(
            name=item['title'],
            artist=item['artist'],
            album=item['album'],
            is_podcast=bool(item['isPodcast']),
            duration=item['duration'].total_seconds(),
        )
        yield track
        
        yield ListenHistory(
            timestamp=item['timestamp'],
            duration=item['listenDuration'].total_seconds(),
            track_id=track.id,
        )