from pymongo import MongoClient


def get_atms(data):
	"""
		Retrieve near ATMs
	:param data: Query data like ATM network and location
	:return: pymongo cursor with result
	"""

	network = data['command'][1:].upper()
	lng = data['location']['longitude']
	lat = data['location']['latitude']

	#TODO: move this to a different module
	db = MongoClient().atmdb6
	
	## this query returns the nearest points
	query = {
				"red": network,
				"location": {
  					"$nearSphere": {
     					"$geometry": {
        					"type" : "Point",
        					"coordinates" : [lng, lat]#[ -58.399125, -34.616312 ]
     					},
     				"$minDistance": 1,
     				"$maxDistance": 500
  					}
				}
	}


	projection = {"banco":1, "dom":1, "location":1, "_id":0}
	
	return db.atmscaba.find(query, projection).limit(3)
