import datetime
import requests
import json

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
	
media_types {
	"com.spotify.music" : "music",
	"com.bambuna.podcastaddict" : "podcast",
}

def call(request, start, end):
	access_token = auth(request)
	url = 'https://api.zenobase.com/buckets/'+request['buckets']['podcasts']+"/"
	params = {
		'constraint_expression':'timestamp:['+start.isoformat()+'..'+end.isoformat()+']'
	}
	headers = {'Authorization': 'Bearer '+access_token}
	response = requests.get(url, params=params, headers=headers)
	print(response.status_code)
	items = json.loads(response.text)
	for item in items['events']:
		
		yield {
			'id': item['@id'],
			'datetime': item['timestamp'][0],
			'action': item['tag'][0],
			'type': media_types[item['tag'][1]],
			'duration': item['duration'],
			'percentage': item['percentage'],
			'title': item['note'][0],
			'album': item['note'][1],
			'artist': item['note'][2],
			
		}