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
	opciones=[]
	menu1='''
¿Por cuál criterio desea ordenar los restaurantes?
1. Coste
2. Clasificaión
3. Distancia Real
0. Salir
'''
	menu2='''
¿En orden ascendente o descendente?
1. Ascendente
2. Descendente
0. Salir
'''

	print(menu1)
	opcion1=input(': ')
	while int(opcion1) not in range(4):
		print('Por favor elija una opcion correcta')
		print(menu1)
		opcion1=input(': ')	
	if opcion1 == '0':
		return False
	elif opcion1 == '1':
		opciones.append('cost')
	elif opcion1 == '2':
		opciones.append('rating')
	elif opcion1 == '3':
		opciones.append('real_distance')

	print(menu2)
	opcion2=input(': ')
	while int(opcion2) not in range(3):
		print('Por favor elija una opcion correcta')
		print(menu2)
		opcion2=input(': ')
	if opcion1 == '0':
		return False
	elif opcion1 == '1':
		opciones.append('asc')
	elif opcion1 == '2':
		opciones.append('desc')

	return opciones

def get_restaurants(city_details,key,num,opciones):
	entity_id=city_details[0]
	entity_type=city_details[1]
	city_name=city_details[2]
	url="https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type={}&start={}&sort={}&order={}".format(entity_id,entity_type,num,opciones[0],opciones[1])
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
		print('Restaurantes de {}'.format(city_details[2]))
	num=0
	opciones=ordenar()
	if not opciones:
		break
	get_restaurants(city_details,key,num,opciones)
	opcion=input("\nDesea seguir viendo restaurantes de {} (s/si, n/no)\n".format(city_details[2]))
	while opcion == "s":
		num+=20
		get_restaurants(city_details,key,num,opciones)
		opcion=input("\nDesea seguir viendo restaurantes de Nueva York (s/si, n/no)\n")
	city=input('Desea introducir otra ciudad para ver sus restaurantes ("0" para salir): ').replace(' ', '%20')