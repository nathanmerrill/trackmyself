import datetime
import requests
import json
from models import SleepHistory

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
            timestamp = datetime.datetime.fromisoformat(item['start'])
            stop = datetime.datetime.fromisoformat(item['end'])
            duration = stop-timestamp
            
            yield SleepHistory(
                ref_id=item['id'],
                timestamp=timestamp,
                stop=stop,
                duration=duration.total_seconds(),
                isNap=duration < datetime.timedelta(hours=3),
            )
        page += 1
        if len(items) != int(response['per_page']):
            return