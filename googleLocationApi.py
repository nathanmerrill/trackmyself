import ijson
import datetime
import math

def findMovement(locations, radius):
	if not locations:
		return
	center = None
	for location in locations:
		if center == None:
			center = location
			continue
		if inRadius(location, center, radius) or location['velocity'] > 0:
			duration = abs(location['datetime'] - center['datetime'])
			yield [center, duration]
			center = location
			
def inRadius(location1, location2, radius):
	return distance(location1['latitude'], location1['longitude'], location2['latitude'], location2['longitude']) <= radius

def distance(x1, y1, x2, y2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def call(filename, start, end):
	with open(filename, 'r') as json:
		locations = ijson.items(json, 'locations.item')
		for location in locations:
			timestamp = location['timestampMs']
			datetime = datetime.datetime.fromtimestamp(int(timestamp)//1000)
			if not (start < datetime < end):
				continue
			yield {
				'datetime': datetime,
				'latitude': int(location['latitudeE7']),
				'longitude': int(location['longitudeE7']),
				'velocity': int(location['velocity']),
			}