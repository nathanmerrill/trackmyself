import datetime
import myFitnessPalApi

mealTimes = {
	"breakfast": datetime.time(7,30),
	"work": datetime.time(11),
	"dinner": datetime.time(18),
	"snacks": datetime.time(17),
	"late night": datetime.time(23),
	"lunch": datetime.time(12),
}

def call(request, start, end):
	for timestamp, meal in myFitnessPalApi.call(request, start, end, "meals", 7):
		time = mealTimes[meal.name.lower()]
		for i, entry in enumerate(meal.entries):
			obj = entry.totals
			obj['date'] = datetime.datetime.combine(timestamp, time)
			obj['meal'] = meal.name
			obj['food'] = entry.name
			yield obj