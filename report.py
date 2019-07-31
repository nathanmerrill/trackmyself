import datetime
import itertools
import apiKeys
import importlib
import storage
import sys

end = datetime.datetime.now()
start = end - datetime.timedelta(days=100)

#Manual work:   
# 1. Fetch audio.txt from phone
# 2. Export daylio from phone
# 3. Download Google location and chat data

# data_sources = ['toggl','daylio','googleLocation','rescueTime','myFitnessPal','audio','hangouts','mint']
data_sources = ['daylio']

tables = []
for data_source in data_sources:
	keys = apiKeys.keys[data_source.lower()]
	libName = data_source+"Api"
	importlib.import_module(libName)
	data = getattr(sys.modules[libName], "call")(keys, start, end)
	storage.store(data)


