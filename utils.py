import atms


def encoding_static_gmap_url(data, atms):
	"""
		Encode the url google map with locations
	"""
	base_url = "https://maps.googleapis.com/maps/api/staticmap?center={},{}&zoom=15&scale=1&size=600x300&maptype=roadmap&format=png&visual_refresh=true".\
					format(data["location"]["latitude"], data["location"]["longitude"])


	for seq, atm in enumerate(atms):
		base_url +=  "&markers=size:mid%7Ccolor:0xff0000%7Clabel:{}%7C{},{}".\
					format(seq+1, atm[0], atm[1])

	
	base_url += "&markers=size:mid%7Ccolor:0x0005ff%7Clabel:A%7C{},{}".\
				format(data["location"]["latitude"], data["location"]["longitude"])

	return base_url


def get_info_atms(data):

	available_atms = atms.get_atms(data)

	output = ""
	coords = []

	for seq, atm in enumerate(available_atms):
		output += """****************\nCajero: {}\nBanco: {}\nDirección: {}\n""".format(seq+1, atm["banco"], atm["dom"])
		coords.append([atm["location"]["coordinates"][1],atm["location"]["coordinates"][0]])

	url_image = encoding_static_gmap_url(data, coords)

	return output, url_image

