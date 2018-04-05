# Ejercicio2. Posibilidad de que la búsqueda anterior se pueda ordenar por un criterio.

import os, requests

def get_request(url,key):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	return r1

def get_city_details(key,city):
	url="https://developers.zomato.com/api/v2.1/locations?query="+city
	r1=get_request(url,key)
	if r1.status_code == 200:
		doc=r1.json()
		if len(doc['location_suggestions']) == 0:
			return False
		else:			
			entity_id=doc['location_suggestions'][0]['entity_id']
			entity_type=doc['location_suggestions'][0]['entity_type']	
			city_name=doc['location_suggestions'][0]['city_name']
			return (entity_id,entity_type,city_name)

def ordenar():
	print('''
		¿Por cuál criterio desea ordenar los restaurantes?
		1. Coste
		2. Clasificaión
		3. Distancia Real
		''')
	criterio=input(': ')
	print('''
		¿En orden ascendente o descendente?
		1. Ascendente
		2. Descendente
		''')
	orden=input(': ')

def get_restaurants(city_details,key,num):
	entity_id=city_details[0]
	entity_type=city_details[1]
	city_name=city_details[2]
	url="https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type={}&start={}".format(entity_id,entity_type,num)
	r1=get_request(url,key)
	if r1.status_code == 200:
		doc = r1.json()		
		if num == 0:
			num_res=doc['results_found']
			print('{} tiene {} restaurantes.\n'.format(city_name,num_res))
		for restaurant in doc['restaurants']:
			print('-->',restaurant['restaurant']['name'])

key=os.environ["key"]

city=input('Ciudad para ver sus restaurantes ("0" para salir): ').replace(' ', '%20')
while city != '0':
	if not get_city_details(key,city):
		print('{} no existe en Zomato'.format(city))
		city=input('Por favor introduzca una ciudad que exista ("0" para salir): ').replace(' ', '%20')
		continue
	else:
		city_details=get_city_details(key,city)

	num=0
	get_restaurants(city_details,key,num)
	opcion=input("\nDesea seguir viendo restaurantes de {} (s/si, n/no)\n".format(city_details[2]))
	while opcion == "s":
		num+=20
		get_restaurants(city_details,key,num)
		opcion=input("\nDesea seguir viendo restaurantes de Nueva York (s/si, n/no)\n")
	city=input('Desea introducir otra ciudad para ver sus restaurantes ("0" para salir): ').replace(' ', '%20')