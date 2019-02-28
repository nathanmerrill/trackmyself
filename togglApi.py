import datetime
import requests
import json

def call(request, start, end):
	url = 'https://toggl.com/reports/api/v2/details'
	auth = requests.auth.HTTPBasicAuth(request['token'],'api_token')
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	page = 1
	while True:
		params = {
			'user_agent': request['user_agent'], 
			'workspace_id': request['workspace_id'], 
			'page': str(page),
			'since': start.isoformat(),
			'until': end.isoformat()
		}
		response = json.loads(requests.get(url, headers=headers, auth=auth, params=params).text)
		if 'error' in response:
			raise Exception(response['error'])
		items = response['data']
		for item in items:
			yield {
				'id': item['id'],
				'name': item['description'], # sleep
				'start': datetime.datetime.fromisoformat(item['start']),
				'end': datetime.datetime.fromisoformat(item['end']), # 2019-02-21T11:40:22-07:00
				'duration': int(item['dur'])/1000, #seconds
			}
		page += 1
		if len(items) != int(response['per_page']):
			return