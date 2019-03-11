import datetime
import requests
import json
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


def formatData(item):
    title, album, artist = tuple(item['note'])        
    action, app = tuple(item['tag'])
    if app not in ('com.bambuna.podcastaddict', 'com.spotify.music'):
        return None
    return {
        'title': title,
        'album': album,
        'artist': artist,
        'action': action,
        'isPodcast': app == 'com.bambuna.podcastaddict',
        'timestamp': datetime.datetime.fromisoformat(item['timestamp'][0][:-1]),
        'duration': datetime.timedelta(seconds=int(item['duration'])/1000),
        'percentage': float(item['percentage']),
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
        

def call(request, start, end):
    access_token = auth(request)
    url = 'https://api.zenobase.com/buckets/'+request['buckets']['podcasts']+"/"
    params = {
        'constraint_expression':'timestamp:['+start.isoformat()+'..'+end.isoformat()+']'
    }
    headers = {'Authorization': 'Bearer '+access_token}
    response = requests.get(url, params=params, headers=headers)
    items = map(formatData, json.loads(response.text)['events'])
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
            listen_duration=item['listenDuration'].total_seconds(),
            track_id=track.id,
        )