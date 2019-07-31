import csv
import datetime
import re
from models import Mood, MoodHistory, Activity, ActivityHistory, ActivityItem

mood_ratings = {
    'excited': 5,
    'productive': 4,
    'fine': 3,
    'bored': 2,
    'awful': 1,
}

activity_map = {
    'game': 'board games',
    'movie': 'tv',
}

def call(filename, start, end):
    moods = dict()
    for name, rating in mood_ratings.items():
        mood = Mood(
            name=name,
            value=rating
        )
        yield mood
        moods[name] = mood
    with open(filename, 'r') as csvfile:
        lines = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(lines)
        for line in lines:
            time = datetime.datetime.strptime(line[0]+' '+line[3], '%Y-%m-%d %I:%M %p')
            if not (start < time < end):
                continue
            yield MoodHistory(
                timestamp=time,
                mood_id=moods[line[4]].id
            )
            
            activities = dict()
            for entry in line[6].split(','):
                entry = entry.strip()
                if len(entry) == 0:
                    continue
                item, value = tuple(entry.split(':'))
                item = formatActivity(item)
                if item not in activities:
                    activities[item] = []
                activities[item].append(value.strip())
                
            for activity in line[5].split(' | '):
                activityName = formatActivity(activity.lower())
                if activityName not in activities:
                    activities[activityName] = []
            
            for activity, items in activities.items():
                activity = Activity(name=activityName)
                yield ActivityHistory(timestamp=time, activity=activity)
                for item in items:
                    yield ActivityItem(name=item, activity=activity)
                    
                    
                    
def formatActivity(activity):
    activity = activity.lower().strip()
    if activity in activity_map:
        activity = activity_map[activity]
    return activity