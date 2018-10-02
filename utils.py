import os

def encoding_static_gmap_url(data, atms):
	"""
		Genera la URL necesaria para que se muestra el mapa
		como una imagen del mapa de Google, con los marlkers de
		la posicion del usuario (azul) y los cajeros cercanos (rojo)
	"""
	base_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=15&scale=1&size=600x600&maptype=roadmap&format=png&visual_refresh=true".\
					format(data["location"]["latitude"], data["location"]["longitude"])


	for seq, atm in enumerate(atms):
		base_url +=  "&markers=size:mid%7Ccolor:0xff0000%7Clabel:{}%7C{},{}".\
					format(seq+1, atm[0], atm[1])

	
	base_url += "&markers=size:mid%7Ccolor:0x0005ff%7Clabel:A%7C{},{}".\
				format(data["location"]["latitude"], data["location"]["longitude"])

	base_url += "&key={}".format(os.environ['API_KEY_GMAP'])

	return base_url


def format_info_atms(data, atms):
	"""
		Genera el output necesario para la consulta
		del cliente
	:param atms: Query
	:return: Tupla con output en forma de texto con la descripcion 
			de los cajeros y la URL del mapa
	"""

	output = ""
	coords = []

	for seq, atm in enumerate(atms):
		output += """****************\nCajero: {}\nBanco: {}\nDirección: {}\n""".format(seq+1, atm["banco"], atm["dom"])
		coords.append([atm["location"]["coordinates"][1],atm["location"]["coordinates"][0]])

	url_image = encoding_static_gmap_url(data, coords)

	return output, url_image

