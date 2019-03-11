import csv
import datetime
import re
from models import Mood, MoodHistory, Activity, ActivityHistory, ActivityItem

mood_ratings = {
    'excited': 5,
    'productive': 4,
    'fine':    3,
    'bored': 2,
    'awful': 1,
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
            parts = re.compile('([a-zA-Z]*\:)').split(line[6])
            activities = dict()
            for item, value in zip(parts, parts[1:]):
                if not item.endswith(':'):
                    continue
                item = item[:-1]
                if item not in activities:
                    activities[item] = []
                activities[item].append(value.strip())
            for activity in line[5].split(' | '):
                if activity not in activities:
                    activities[activity] = []
            
            for activity, items in activities.items():
                activity = Activity(name=activity)
                yield activity
                yield ActivityHistory(timestamp=time, activity_id=activity.id)
                for item in items:
                    yield ActivityItem(name=item, activity_id=activity.id)
            