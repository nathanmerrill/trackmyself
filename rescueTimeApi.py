import datetime
import requests
import json

def call(request, start, end):
	url = 'https://www.rescuetime.com/anapi/data'
	while True:
		params = {
			'key': 	request['token'],
			'format': 'json',
			'perspective': 'interval',
			'resolution_time': 'minute',
			'restrict_begin': start.isoformat(),
			'restrict_end': end.isoformat(),
			'restrict_kind': 'document'
		}
		response = json.loads(requests.get(url, params=params).text)
		if 'error' in response:
			raise Exception(response['error'])
		yield response
		items = response['rows']
		for item in items:
			yield {
				"datetime": datetime.datetime.fromisoformat(item[0]),
				"duration": int(item[1]), #seconds
				"activity": item[2], #Url or app name
				"document": item[3], #Page title or app title
				"category": item[4], #"General Entertainment" or "Productivity", etc
				"productivity": int(item[5]), #between 2 and -2
			}
			