import requests
from math import cos, asin, sqrt  
from time import sleep
#see https://www.adsbexchange.com/datafields/ for field explanations
#Input your latitude and longitude
my_lat =
my_long =
#how far of a radius in KM from my_lat and my_long you want to search for aircraft.  Useful for limiting search results
range = 8
aircraft_list = []

def get_all_aircraft():
	request = requests.get('https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat='+ str(my_lat) + 'lng='+ str(my_long) + 'fDstL=0&fDstU='+str(range))	
	nearby_aircaft = request.json()
	nearby_aircaft = nearby_aircaft['acList']
	# for aircraft in nearby_aircaft:
		# print aircraft
	return nearby_aircaft

def distance(lat1, lon1, lat2, lon2):  #haversine formula https://stackoverflow.com/questions/41336756/find-the-closest-latitude-and-longitude
    p = 0.017453292519943295  #Pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a)) #2*R*asin.. 


def display_aircraft():
	aircraft_list = []
	aircraft_list_from_website = get_all_aircraft()

	for aircraft in aircraft_list_from_website:
		aircraft_id = aircraft['Id']
		if 'Mdl' in aircraft:
			aircaft_mdl = aircraft['Mdl']
		else:
			aircaft_mdl = False
		if 'Op' in aircraft:
			aircaft_op = aircraft['Op']
		else:
			aircaft_op = False
		# aircaft_flight_no = aircraft['Op']
		if 'From' in aircraft:
			aircaft_origin = aircraft['From']
		else:
			aircaft_origin = 'No Origin Info'
		if 'To' in aircraft:
			aircraft_dest = aircraft['To']
		else:
			aircraft_dest = 'No Destination Info'
		if 'Call' in aircraft:
			aircraft_call = aircraft['Call']
		else:
			aircraft_call = False
		if 'GAlt'in aircraft:
			aircaft_alt = aircraft['GAlt'] #ground alt in feet
		else:
			aircaft_alt = False
		if 'Spd' in aircraft:
			aircaft_speed = aircraft['Spd']
		else: 
			aircaft_speed = False
		if 'Lat' in aircraft:
			aircaft_lat = aircraft['Lat']
		else:
			aircaft_lat	= False
		if 'Long' in aircraft:
			aircaft_long = aircraft['Long']
		else:
			aircaft_long = False
		
		
		aircraft_distance = distance(my_lat, my_long, aircaft_lat, aircaft_long)
		aircraft_list.append({'Id': aircraft_id, 'Mdl': aircaft_mdl, 'Op': aircaft_op, 
			'From': aircaft_origin, 'To': aircraft_dest, 'Call': aircraft_call, 'Alt': aircaft_alt, 'Spd': aircaft_speed, 'Distance': aircraft_distance})
	aircraft_list = sorted(aircraft_list, key=lambda k: k ['Distance'])
#	print aircraft_list
	try:
		return aircraft_list[0]
	except IndexError:
		return 'No aircraft within',range,'km'
	# print "---------"	
	# print aircraft['Op']
	
# for aircraft in aircraft_list:
	# print aircraft
#display_aircraft()
while 1:	
	print display_aircraft()
	sleep(5)
