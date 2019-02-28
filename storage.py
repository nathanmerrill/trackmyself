import sqlite3


class Db:
	def __init__(self, conn):
		self.conn = conn
		self.cursor = con.cursor()
	
	def _createTable(name, columns):
		self.conn.execute("CREATE TABLE IF NOT EXISTS "+name+"(\n"+"\n".join(columns)+"\n);")
	
	def _defineColumn(name=None, type=None, length=50, primaryKey=False, foreignKey = None):
		if name == None:
			if primaryKey:
				name = "id"
			else:
				raise Exception("name requred")
		if primaryKey and type is None:
			return name+" INTEGER PRIMARY KEY("+name+") ON CONFLICT REPLACE AUTOINCREMENT"
		elif primaryKey:
			return name+" "+type+" PRIMARY KEY("+name+") ON CONFLICT REPLACE"
		if type is None:
			type = "VARCHAR("+length+")"
		if foreignKey is None:
			return name+" "+type
		else:
			return name+" "+type
	
	def _defineForeignKey(column, foreignTable, foreignColumn):
		

class Mood(Db):
	def createTable():
		
		

def store(source_type, data):
	conn = sqlite3.connect('quantifiedSelf.db')
	
def createMood():
	"""CREATE TABLE IF NOT EXISTS mood (
		id INTEGER PRIMARY KEY(id) ON CONFLICT REPLACE AUTOINCREMENT,
		moodRating
		mood VARCHAR(20)
	)"""
def storeDaylio(data):
	for datum in data:
		"""INSERT into mood (