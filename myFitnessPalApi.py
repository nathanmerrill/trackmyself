import datetime
import myfitnesspal

days = dict()

def call(request, start, end, attribute, timeout):
	client = myfitnesspal.Client(request['username'], request['password'])
	dayCount = (end - start).days + 1
	date = start.date()
	emptyDays = 0
	for i in reversed(range(dayCount)):
		timestamp = date + datetime.timedelta(days=i)
		if timestamp in days:
			day = days[timestamp]
		else:
			day = client.get_date(timestamp)
		items = getattr(day, attribute)
		if all(len(item) == 0 for item in items):
			emptyDays += 1
			if emptyDays == timeout:
				return
			continue
		else:
			emptyDays = 0
		for item in items:
			yield (timestamp, item)