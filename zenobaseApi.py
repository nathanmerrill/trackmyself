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
    for item in items:
        if 'listenDuration' not in item:
            item['listenDuration'] = item['duration']
        if last is None:
            last = item
            continue
        maximumDuration = item['timestamp'] - last['timestamp']
        if item['listenDuration'] > maximumDuration:
            item['listenDuration'] = maximumDuration
        yield item        

def mergeItems(items):
    for sequence in findSequences(items):
        last = None
        for current in sequence:
            if last is None:
                last = current                
                continue
            
            listenDuration = (current['timestamp'] - last['timestamp']).total_seconds()
            
            if current['action'] == last['action'] and listenDuration > last['duration'].total_seconds()*.9:
                yield last
                last = current
                continue
            
            if current['action'] == 'stop':
                last['listenDuration'] = current['duration']*(current['percentage'] - last['percentage'])
            else :
                del last['listenDuration']
        yield last


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
        'duration': datetime.timedelta(seconds=int(item['duration'])),
        'percentage': float(item['percentage']),
    }
    
def findSequences(items):
    currentTrack = None
    next = []
    for item in items:
        if item is None:
            continue
        if currentTrack != item['title']:
            if currentTrack is not None:
                yield next
                next = []
            currentTrack = item['title']
            next.append(item)
            continue
    if currentTrack is not None:
        yield next
        

def call(request, start, end):
    
    access_token = auth(request)
    url = 'https://api.zenobase.com/buckets/'+request['buckets']['podcasts']+"/"
    params = {
        'constraint_expression':'timestamp:['+start.isoformat()+'..'+end.isoformat()+']'
    }
    headers = {'Authorization': 'Bearer '+access_token}
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code)
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