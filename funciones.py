
def get_city(key):
	while True:
		city=input("Ciudad para ver sus restaurantes")
		city1=city.replace(' ','%20')
		cabecera={"Accept": "application/json", "user-key": key  }
		url="https://developers.zomato.com/api/v2.1/locations?query="+city1
		r1=requests.get(url,headers=cabecera)

		if r1.status_code == 200:
			doc=r1.json()

		if len(doc['location_suggestions']) == 0:
			print('Esta ciudad no existe')
			continue
		else:
			entity_type=doc['location_suggestions'][0]['entity_type']
			entity_id=doc['location_suggestions'][0]['entity_id']
			return [entity_type,entity_id]
			break

