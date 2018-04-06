## 3. Buscar restaurantes en la ciudad de Nueva York,introduciendo filtros 
## de categoría, colecciones, tipos de cocina, tipos de locales y cadenas de texto.

##-- bash> export key="090e1edd54fa3019b80ac170096eb4f4"

import sys, os, requests

def get_request(url,key):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	return r1

def get_list_criterio(key,crit):
	if crit=="categories":
		url="https://developers.zomato.com/api/v2.1/categories"
	else:
		url="https://developers.zomato.com/api/v2.1/{}?city_id=280".format(crit)
	r1=get_request(url,key)
	if r1.status_code == 200:
		doc = r1.json()
		return doc

def mostrar_list_criterio(doc,crit,crits):
	print('\nCriterio {} en Zomato: \n'.format(crit))
	for criterio,num in zip(doc[crit],range(len(doc[crit]))):
		print('{} --> {}'.format(num+1,criterio[crits[0]][crits[2]]))

def elegir_opcion_criterio(doc,crit):
	try:
		opcion=int(input('\nElije un número de la lista de {}: ("0" para salir): '.format(crit)))
		if opcion not in range(len(doc[crit])+1):
			print('Por favor elija un número de la lista')
			return elegir_opcion_criterio(doc,crit)
		elif opcion == 0:
			return False
		else:
			return opcion
	except ValueError:
		print('Por favor introduzca un número.')
		return elegir_opcion_criterio(doc,crit)
	except KeyboardInterrupt:
		print("\nAdios!")
		sys.exit()

def elegir_criterio(key,crit,crits):
	doc=get_list_criterio(key,crit)
	mostrar_list_criterio(doc,crit,crits)
	opciones=[]
	opcion=elegir_opcion_criterio(doc,crit)
	while opcion:
		opciones.append(opcion)
		opcion=elegir_opcion_criterio(doc,crit)
	ids_criterios=[]
	for opcion in opciones:
		criterio_id=doc[crit][opcion-1][crits[0]][crits[2]]
		ids_criterios.append(criterio_id)
	return ids_criterios

key=os.environ["key"]
criterios=[{"categories":["categories","id","name"]},{"collections":["collection","collection_id","title"]},{"cuisines":["cuisine","cuisine_id","cuisine_name"]},{"establishments":["establishment","id","name"]}]

for i in criterios:
	for crit,crits in i.items():
		ids_criterios=elegir_criterio(key,crit,crits)
		for i in ids_criterios:
			print(i)















#get_restaurants(key,num)
#
#
#def get_restaurants(key,num):
#	url="https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city&start={}&cuisines=1%2C2%2C3&establishment_type=1%2C2%2C3&collection_id=1%2C2%2C3&category=1%2C2%2C3".format(num)
#	r1=get_request(url,key)
#	if r1.status_code == 200:
#		doc = r1.json()		
#		if num == 0:
#			num_res=doc['results_found']
#			print('{} tiene {} restaurantes.\n'.format(city_name,num_res))
#		for restaurant in doc['restaurants']:
#			print('-->',restaurant['restaurant']['name'])