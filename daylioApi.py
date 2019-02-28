import csv
import datetime

mood_ratings = {
	'excited': 5,
	'productive': 4,
	'fine':	3,
	'bored': 2,
	'awful': 1,
}

def call(filename, start, end):
	with open(filename, 'r') as csvfile:
		lines = csv.reader(csvfile, delimiter=',', quotechar='"')
		next(lines)
		for line in lines:
			time = datetime.datetime.strptime(line[0]+' '+line[3], '%Y-%m-%d %H:%M')
			if not (start < time < end):
				continue
			yield {
				'datetime': time,
				'mood': line[4], # productive
				'activities': line[5]
			}