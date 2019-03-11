import datetime
import itertools
import apiKeys
import importlib
import storage
import sys



end = datetime.datetime.now()
start = end - datetime.timedelta(days=30)

# data_sources = ['toggl','daylio','googleLocation','rescueTime','myFitnessPalFood','myFitnessPalExercise','zenobase','hangouts','mint']

data_sources = ['daylio']

tables = []
for data_source in data_sources:
	keys = apiKeys.keys[data_source]
	libName = data_source+"Api"
	importlib.import_module(libName)
	data = getattr(sys.modules[libName], "call")(keys, start, end)
	storage.store(data)

    
    

# Datasources rules:
# File sources take a filename
# API sources take a request object, start datetime, and end datetime
# Return a generator
# Each item generated has an ID
# Datetime used for all timestamps
# Durations in seconds

# data = togglApi.call(requests['toggl'], start, end)
# data = daylioApi.call(files['daylio'], start, end)
# data = googleLocationApi.findMovement(googleLocationApi.call(files['googleLocation'], start, end), 300)
# data = rescueTimeApi.call(requests['rescuetime'], start, end)
# data = myFitnessPalFoodApi.call(requests['myfitnesspal'], start, end)
# data = myFitnessPalExerciseApi.call(requests['myfitnesspal'], start, end)
# data = zenobaseApi.call(requests['zenobase'], start, end)
# data = hangoutsApi.call(files['hangouts'], start, end)
# data = mintApi.call(requests['mint'], start, end)
# data = spotifyApi.call(requests['spotify'], start, end)

# for item in itertools.islice(data,1000):
	# print(item)


