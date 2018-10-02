import numpy as np
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler


class ATMManager(object):
	"""docstring for chat"""
	def __init__(self, host="localhost", port=27017):
		super(ATMManager, self).__init__()
		self.host = host
		self.port = port
		self.db = MongoClient(host, port).atmdb
		
	def reload_atms(self):
		"""
		Recarga los cajeros que están po debajo
		su nivel de extracciones.
		"""

		self.db.atmscaba.update_many(
			{
				"extracciones": {
					"$lt": 1000	
				}
			},
			{ 
				"$set": {
					"extracciones": 1000
				}
			}
		)

	def launch_bg_process(self):
		"""
			Planifica una tarea para recargar los cajeros
			los dias de semana a las 8am.
		"""
		print("Lanzando proceso de recarga de cajeros en background")
		sched = BackgroundScheduler()
		sched.add_job(self.reload_atms, 'cron', day_of_week='mon-fri', hour=8)
		sched.start()

	def extract_money(self,atms):
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

		self.db.atmscaba.update_one({"id":id_atm},{"$inc":{"extracciones": -1}})

	def get_atms(self,data):
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
		
		## this query returns the nearest points
		query = {
					"extracciones": {
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


		projection = {"id":1, "banco":1, "dom":1, "location":1, "extracciones":1, "_id":0}

		result = list(self.db.atmscaba.find(query, projection).limit(3))

		if len(result):
			self.extract_money(result)

		return result
