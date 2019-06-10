import datetime
import requests
import json
from models import ElectronicActivity, ElectronicActivityHistory

def call(request, start, end):
    url = 'https://www.rescuetime.com/anapi/data'
    params = {
        'key': request['token'],
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
    items = response['rows']
    headers = dict((x, i) for i, x in enumerate(response['row_headers']))
    for item in items:
        activity = ElectronicActivity(name=item[headers['Activity']], productivity_score=int(item[headers['Productivity']]), category=item[headers['Category']])
        yield activity
        page_title = item[headers['Document']]
        if page_title == "No Details":
            page_title = None
        yield ElectronicActivityHistory(
            timestamp=datetime.datetime.fromisoformat(item[headers['Date']]),
            activity_id=activity.id, 
            duration=int(item[headers['Time Spent (seconds)']]), 
            page_title=page_title
        )
            