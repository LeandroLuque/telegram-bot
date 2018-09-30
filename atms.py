import numpy as np
from pymongo import MongoClient


def reload_atms():
	"""
		Recarga los cajeros que están po debajo
		su nivel de extracciones.
	"""

	db = MongoClient().atmdb7

	db.atmscaba.update_many(
	    {"extractions": {
	    	"$lt": 5	
	    }},
	    { "$set":
	      {
	        "extractions": 5
	      }
	   }
	)

def extract_money(db, atms):
	"""
		Extrae dinero de un cajero de acuerdo a
		cierta probabilidad
	:param db:Conección con la BD.
	:param atms: Pymongo cursor con los resultados
	:param p: Número que indica de cual cajero sacar
	"""

	if len(atms) == 3:
		id_atm = np.random.choice(atms, p=[0.7, 0.2, 0.1])["id"]
	elif len(atms) == 2:
		id_atm = np.random.choice(atms, p=[0.7, 0.3])["id"]
	else:
		id_atm = atms[0]["id"]

	db.atmscaba.update_one({"id":id_atm},{"$inc":{"extractions": -1}})

def get_atms(data):
	"""	
		Retorna los cajeros más cercano a la posicion del
		usuario, que tengan dinero disponible, en un radio de 
		500 mts.
	:param data: Dictionario con datos del chat, como tipo de cajero
					y ubicación
	:return: Pymongo cursor con resultados, ordenados por cercania
			a la posición enviada.
	"""

	network = data['command'][1:].upper()
	lng = data['location']['longitude']
	lat = data['location']['latitude']

	#TODO: move this to a different module
	db = MongoClient().atmdb7
	
	## this query returns the nearest points
	query = {
				"extractions": {
					"$gt": 0
				},
				"red": network,
				"location": {
  					"$nearSphere": {
     					"$geometry": {
        					"type" : "Point",
        					"coordinates" : [-58.429863,-34.593244]#[lng, lat]
     					},
     				"$minDistance": 1,
     				"$maxDistance": 500
  					}
				}
	}


	projection = {"id":1, "banco":1, "dom":1, "location":1, "extractions":1, "_id":0}

	result = list(db.atmscaba.find(query, projection).limit(3))

	if len(result):
		extract_money(db, result)

	return result