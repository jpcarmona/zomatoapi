## 3. Buscar restaurantes en la ciudad de Nueva York,introduciendo filtros 
## de categoría, colecciones, tipos de cocina, tipos de locales y cadenas de texto.

##-- bash> export key="090e1edd54fa3019b80ac170096eb4f4"

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

def get_url(cadena):
	url="https://developers.zomato.com/api/v2.1/search?entity_id=280&entity_type=city&q={}".format(cadena)
	return url

def get_request(url,key):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	return r1

def get_request_filtro(key,f1):
	if f1=="categories":
		url="https://developers.zomato.com/api/v2.1/categories"
	else:
		url="https://developers.zomato.com/api/v2.1/{}?city_id=280".format(f1)
	r1=get_request(url,key)
	if r1.status_code == 200:
		doc = r1.json()
		return doc

def mostrar_list_filtro(doc,f1,f2):
	print('\nFiltro {} en Zomato: \n'.format(f1))
	for filtro,num in zip(doc[f1],range(len(doc[f1]))):
		print('{} --> {}'.format(num+1,filtro[f2[0]][f2[2]]))

def elegir_opcion_filtro(doc,f1):
	try:
		opcion=int(input('\nElije un número de la lista de {}: ("0" para salir): '.format(f1)))
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

def elegir_filtro(doc,f1,f2):
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

def get_requests_restaurants(key,url,num="0",url1=''):
	url2=url+'&start='+num+url1
	r1=get_request(url2,key)
	if r1.status_code == 200:
		doc = r1.json()
		if len(doc['restaurants']) == 0:
			return False
		else:
			return doc['restaurants']

def get_url_filtro(lista_filtros,f1,f2):
	ids_filtros=elegir_filtro(lista_filtros,f1,f2)
	url1='&{}={}'.format(f2[3],"%2C".join(map(str,ids_filtros)))
	return url1

def lista_restaurantes(key,url):
	num=0
	lista_rest=[]
	get_req=get_requests_restaurants(key,url,str(num))
	while get_req:		
		lista_rest+=get_req
		num+=20
		get_req=get_requests_restaurants(key,url,str(num))
	return lista_rest

def mostrar_restaurants(lista_rest):
	num=0
	for restaurant in lista_rest:
		num+=1
		print(num,'-->',restaurant['restaurant']['name'])
	return num

key=os.environ["key"]

filtros=[]
filtros.append({"cuisines":["cuisine","cuisine_id","cuisine_name","cuisines"]})
filtros.append({"establishments":["establishment","id","name","establishment_type"]})
filtros.append({"collections":["collection","collection_id","title","collection_id"]})
filtros.append({"categories":["categories","id","name","category"]})

lista_res_final=[]
cadena=input('\nNombre de restaurante que desea buscar ("0" para salir): ')
while cadena != "0":
	url=get_url(cadena)
	get_req=get_requests_restaurants(key,url)
	if not get_req:
		print("Este nombre de restaurante no se encuentra en zomato.")
		pass
	else:
		lista_res_final=lista_restaurantes(key,url)
		print('\nSe han encontrado {} restaurantes que tengan en su nombre "{}".'.format(len(lista_res_final),cadena))
		for i in filtros:
			print('\n¿Desea seguir aplicando filtros? ("s"/SI "n"/NO)')
			opcion=seguir()
			if opcion:
				pass
			else:
				break			
			for f1,f2 in i.items():
				lista_res_final=[]
				lista_filtros=get_request_filtro(key,f1)
				mostrar_list_filtro(lista_filtros,f1,f2)
				url1=get_url_filtro(lista_filtros,f1,f2)
				get_req=get_requests_restaurants(key,url+url1)
				while not get_req:
					print("No se han encontrado restaurantes con los filtros indicados hasta el momento.")
					print('\n¿Desea volver a aplicar filtros en {}? ("s"/SI "n"/NO)'.format(f1))
					opcion=seguir()
					if opcion:
						url1=get_url_filtro(lista_filtros,f1,f2)
						get_req=get_requests_restaurants(key,url+url1)
					else:
						break
				if not get_req:
					pass
				else:
					url=url+url1
					lista_rest=lista_restaurantes(key,url)
					lista_res_final+=lista_rest
					print('\nSe han encontrado {} restaurantes con los filtros indicados hasta el momento.'.format(len(lista_res_final)))
			if not get_req:
				break
	if lista_res_final:
		mostrar_restaurants(lista_res_final)
	cadena=input('\nOtro nombre de restaurante que desee buscar ("0" para salir): ')




