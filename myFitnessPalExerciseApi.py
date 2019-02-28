import datetime
import myFitnessPalApi

def call(request, start, end):
	for timestamp, exercise in myFitnessPalApi.call(request, start, end, "exercises", 7):
		for i, entry in enumerate(exercise.entries):
			obj = entry.totals
			obj['date'] = datetime.datetime.combine(timestamp, datetime.time(0))
			obj['type'] = entry.name
			yield obj