import pandas as pd
from pymongo import MongoClient, GEOSPHERE

def populate(db):
	"""
		Pobla la Mongo DB con los datos del dataset
	"""
	
	df = pd.read_csv('dataset/cajeros-automaticos.csv', sep=";")
	df = df[['ID', 'LAT', 'LNG', 'BANCO', 'RED', 'DOM_ORIG']]

	df['LAT'] = df['LAT'].apply(lambda x: float(x.replace(',', '.')))
	df['LNG'] = df['LNG'].apply(lambda x: float(x.replace(',', '.')))

	values = [
		{
			"extracciones": 1000,
			"location":{"type":"Point", "coordinates": [x[2], x[1]]},
			"id":x[0], 
			"banco":x[3], 
			"red":x[4], 
			"dom":x[5]
		}
		for x in df.values
	]

	db.atmscaba.insert_many(values)

	db.atmscaba.create_index([("location", GEOSPHERE)])


def init_db():
	"""
		Conección con la DB.
	"""

	print("Iniciando DB")

	client = MongoClient('mongo', 27017)
	db = client['atmdb']

	if db.atmscaba.find().count() == 0:
		populate(db)

	client.close()