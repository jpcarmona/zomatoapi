## 3. Buscar restaurantes en la ciudad de Nueva York,introduciendo metodos 
## de categoría, colecciones, tipos de cocina, tipos de locales y cadenas de texto.

import sys, os, requests

def seguir():
	try:
		opcion=input(': ')
		if opcion not in ("s","n"):
			print('Por favor elija "s" o "n"')
			return seguir()
		elif opcion == "n":
			return False
		else :
			return True
	except KeyboardInterrupt:
		print("\nAdios!")
		sys.exit()

def elegir_opcion_filtro(doc,f1):
	try:
		opcion=int(input('\nElije un número de la lista de {}: ("0" para terminar): '.format(f1)))
		if opcion not in range(len(doc[f1])+1):
			print('Por favor elija un número de la lista')
			return elegir_opcion_filtro(doc,f1)
		elif opcion == 0:
			return False
		else:
			return opcion
	except ValueError:
		print('Por favor introduzca un número.')
		return elegir_opcion_filtro(doc,f1)
	except KeyboardInterrupt:
		print("\nAdios!")
		sys.exit()



def get_requests(key,url):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	if r1.status_code == 200:
		doc = r1.json()
		return doc

def get_requests_restaurants(key,url,num="0",url1=''):
	url2=url+'&start='+num+url1
	doc=get_requests(key,url2)
	return doc



def mostrar_restaurants(doc,num):
	for restaurant in doc['restaurants']:
		num+=1
		print(num,'-->',restaurant['restaurant']['name'])

def mostrar_restaurantes(key,url1,url2=''):
	num=0
	doc=get_requests_restaurants(key,url1,str(num),url2)
	mostrar_restaurants(doc,num)
	while len(doc['restaurants'])==20 and num!=80:
		print('\n¿ Desea seguir viendo restaurantes ? ("s"/SI "n"/NO)')
		opcion=seguir()
		if opcion:
			num+=20
			doc=get_requests_restaurants(key,url1,str(num),url2)
			mostrar_restaurants(doc,num)
		else:
			break

def mostrar_lista_metodo(doc,metod):
	f1=metod[0]
	f2=metod[1]
	print('\nFiltro {} en Zomato: \n'.format(f1))
	os.system("sleep 1")
	for filtro,num in zip(doc[f1],range(len(doc[f1]))):
		print('{} --> {}'.format(num+1,filtro[f2[0]][f2[2]]))



def elegir_filtros_metodo_cocina(doc,metod):
	f1=metod[0]
	f2=metod[1]
	opciones=[]
	opcion=elegir_opcion_filtro(doc,f1)
	while opcion:
		opciones.append(opcion)
		opcion=elegir_opcion_filtro(doc,f1)
	ids_filtros=[]
	for opcion in opciones:
		filtro_id=doc[f1][opcion-1][f2[0]][f2[1]]
		ids_filtros.append(filtro_id)
	return ids_filtros

def elegir_filtros_metodos(doc,metod):
	f1=metod[0]
	f2=metod[1]
	opcion=elegir_opcion_filtro(doc,f1)
	filtro_id=doc[f1][opcion-1][f2[0]][f2[1]]
	return filtro_id



def get_url(cadena):
	url="https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city&q={}".format(cadena)
	return url

def url_nombre(key):
	try:
		cadena=input('\nNombre de restaurante que desee buscar: ')
		url=get_url(cadena)
		doc=get_requests(key,url)
		resultados=doc['results_found']
		if resultados == '0':
			print('No se han encontrado restaurantes con el nombre "{}'.format(cadena))
			return False
		else:
			print('\nSe han encontrado {} restaurantes con el nombre "{}"'.format(resultados,cadena))
			os.system("sleep 1")
			return url
	except KeyboardInterrupt:
		print("\nAdios!")
		sys.exit()

def url_cocina(key,doc,metod):
	ids_filtroscocina=elegir_filtros_metodo_cocina(doc,metod)
	f2=metod[1]
	url='&{}={}'.format(f2[3],"%2C".join(map(str,ids_filtroscocina)))
	return url

def url_metodos(key,doc,metod):
	filtro_id=elegir_filtros_metodos(doc,metod)
	f2=metod[1]
	url='&{}={}'.format(f2[3],filtro_id)
	return url



def filtrar_metodo_nombre(key):
	url=url_nombre(key)
	while not url:
		print('¿ Desea seguir buscando nombres de restaurantes ? ("s"/SI "n"/NO)')
		opcion=seguir()
		if opcion:
			url=url_nombre(key)
		else:
			break
	if url:
		return url
	else:
		return False

def filtrar_metodo1_cocina(key,url,metod):
	url1="https://developers.zomato.com/api/v2.1/{}?city_id=280".format(metod[0])
	doc=get_requests(key,url1)
	mostrar_lista_metodo(doc,metod)	
	url2=url_cocina(key,doc,metod)
	url3=url+url2
	doc1=get_requests(key,url3)
	resultados=doc1['results_found']
	if resultados == '0':
		print('\nNo se han encontrado restaurantes con los filtros aplicados.\n')
		return False
	else:
		print('\nSe han encontrado {} restaurantes con los filtros aplicados.\n'.format(resultados))
		return url2

def filtrar_metodo2_categoria(key,url,metod):
	url1="https://developers.zomato.com/api/v2.1/categories"
	doc=get_requests(key,url1)
	mostrar_lista_metodo(doc,metod)	
	url2=url_metodos(key,doc,metod)
	url3=url+url2
	doc1=get_requests(key,url3)
	resultados=doc1['results_found']
	if resultados == '0':
		print('\nNo se han encontrado restaurantes con los filtros aplicados.\n')
		return False
	else:
		print('\nSe han encontrado {} restaurantes con los filtros aplicados.\n'.format(resultados))
		return url2

def filtrar_metodo3_establecimiento(key,url,metod):
	url1="https://developers.zomato.com/api/v2.1/{}?city_id=280".format(metod[0])
	doc=get_requests(key,url1)
	mostrar_lista_metodo(doc,metod)	
	url2=url_metodos(key,doc,metod)
	url3=url+url2
	doc1=get_requests(key,url3)
	resultados=doc1['results_found']
	if resultados == '0':
		print('\nNo se han encontrado restaurantes con los filtros aplicados.\n')
		return False
	else:
		print('\nSe han encontrado {} restaurantes con los filtros aplicados.\n'.format(resultados))
		return url2



def filtrar_metodo1(key,metod):
	url1=filtrar_metodo_nombre(key)
	if not url1:
		url2='https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city'
	else:
		url2=url1
	url3=filtrar_metodo1_cocina(key,url2,metod)
	while not url3:
		print('¿ Desea seguir aplicando filtros de cocina ? ("s"/SI "n"/NO)')
		opcion=seguir()
		if opcion:
			url3=filtrar_metodo1_cocina(key,url2,metod)
		else:
			break
	if url1 and not url3:
		mostrar_restaurantes(key,url1)
	else:
		mostrar_restaurantes(key,url2,url3)

def filtrar_metodo2(key,metod):
	url1=filtrar_metodo_nombre(key)
	if not url1:
		url2='https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city'
	else:
		url2=url1
	url3=filtrar_metodo2_categoria(key,url2,metod)
	while not url3:
		print('¿ Desea volver a aplicar un filtro de categoria ? ("s"/SI "n"/NO)')
		opcion=seguir()
		if opcion:
			url3=filtrar_metodo2_categoria(key,url2,metod)
		else:
			break
	if url1 and not url3:
		mostrar_restaurantes(key,url1)
	else:
		mostrar_restaurantes(key,url2,url3)

def filtrar_metodo3(key,metod):
	url1=filtrar_metodo_nombre(key)
	if not url1:
		url2='https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city'
	else:
		url2=url1
	url3=filtrar_metodo3_establecimiento(key,url2,metod)
	while not url3:
		print('¿ Desea volver a aplicar un filtro de establecimiento ? ("s"/SI "n"/NO)')
		opcion=seguir()
		if opcion:
			url3=filtrar_metodo3_establecimiento(key,url2,metod)
		else:
			break
	if url1 and not url3:
		mostrar_restaurantes(key,url1)
	else:
		mostrar_restaurantes(key,url2,url3)

def filtrar_metodo4(key,metod):
	url2='https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city'
	url3=filtrar_metodo3_establecimiento(key,url2,metod)
	while not url3:
		print('¿ Desea volver a aplicar un filtro de establecimiento ? ("s"/SI "n"/NO)')
		opcion=seguir()
		if opcion:
			url3=filtrar_metodo3_establecimiento(key,url2,metod)
		else:
			break
	mostrar_restaurantes(key,url2,url3)



def filtrar_metodos(key,metodo,metodos):
	metod=metodos[int(metodo)-1]
	if metodo == '1':
		filtrar_metodo1(key,metod)
	elif metodo == '2':
		filtrar_metodo2(key,metod)
	elif metodo == '3':
		filtrar_metodo3(key,metod)
	elif metodo == '4':
		filtrar_metodo4(key,metod)	

def elegir_metodo():
	print('\nPor favor elija un método de búsqueda:')
	print(
'''1. Por nombre de restaurante y tipos de cocina.
2. Por nombre de restaurante y categoria.
3. Por nombre de restaurante y tipo establecimiento.
4. Por colecciones. 
0. Salir. ''')
	try:
		metodo=input(': ')
		if int(metodo) not in range(5):
			print('Por favor elija una opcion de la lista.')
			return elegir_metodo()
		else:
			return metodo
	except ValueError:
		print('Por favor introduzca un número.')
		return elegir_metodo()
	except KeyboardInterrupt:
		print("\nAdios!")
		sys.exit()



print('BIENVENIDO AL BUSCADOR DE RESTAURANTES DE ZOMATO!')

key=os.environ["key"]

metodos=[]
metodos.append(["cuisines",["cuisine","cuisine_id","cuisine_name","cuisines"]])
metodos.append(["categories",["categories","id","name","category"]])
metodos.append(["establishments",["establishment","id","name","establishment_type"]])
metodos.append(["collections",["collection","collection_id","title","collection_id"]])


metodo=elegir_metodo()
while metodo !='0':	
	filtrar_metodos(key,metodo,metodos)
	metodo=elegir_metodo()
