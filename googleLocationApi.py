import ijson
import datetime
import math

from models import Location, LocationHistory

def findMovement(locations, radius):
    center = None
    for location in locations:
        if center == None:
            center = location
            continue
        if not inRadius(location, center, radius) or location['velocity'] > 0:
            yield (center, center['datetime'] - location['datetime'])
            center = location

def inRadius(location1, location2, radius):
    return distance(location1['latitude'], location1['longitude'], location2['latitude'], location2['longitude']) <= radius

def distance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
def formatLocation(location):
    return {
        'datetime': datetime.datetime.fromtimestamp(int(location['timestampMs'])//1000),
        'latitude': int(location['latitudeE7']),
        'longitude': int(location['longitudeE7']),
        'velocity': int(location.get('velocity') or 0),        
    }

def call(filename, start, end):
    with open(filename, 'r') as json:
        locations = map(formatLocation, ijson.items(json, 'locations.item'))
        for location, duration in findMovement(locations, 20):
            if location['datetime'] < start:
                continue
            if location['datetime'] > end:
                return
            model = Location(lat=location['latitude'], long=location['longitude'])
            yield model
            yield LocationHistory(
                location_id=model.id,
                timestamp=location['datetime'],
                velocity=location['velocity'],
                duration=duration.seconds
            )