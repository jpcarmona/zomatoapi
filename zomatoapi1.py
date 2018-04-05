# 1. Posibilitar buscar restaurantes en otra ciudad.

##-- bash> export key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

import os
from funciones import get_city, get_restaurants

key=os.environ["key"]

city=input('Ciudad para ver sus restaurantes ("0" para salir): ').replace(' ', '%20')
while city != '0':
	if not get_city(key,city):
		print('{} no existe en Zomato'.format(city))
		city=input('Por favor introduzca una ciudad que exista ("0" para salir): ').replace(' ', '%20')
		continue
	else:
		entity_city=get_city(key,city)
	num=0
	get_restaurants(entity_city,key,num)
	opcion=input("\nDesea seguir viendo restaurantes de {} (s/si, n/no)\n".format(entity_city[2]))
	while opcion == "s":
		num+=20
		get_restaurants(entity_city,key,num)		
		opcion=input("\nDesea seguir viendo restaurantes de Nueva York (s/si, n/no)\n")
	city=input('Desea introducir otra ciudad para ver sus restaurantes ("0" para salir): ').replace(' ', '%20')

