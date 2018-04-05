import requests

def get_request(url,key):
	cabecera={"Accept": "application/json", "user-key": key}
	r1=requests.get(url,headers=cabecera)
	return r1

def get_city(key,city):
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

def get_restaurants(entity_city,key,num):
	entity_id=entity_city[0]
	entity_type=entity_city[1]
	city_name=entity_city[2]
	url="https://developers.zomato.com/api/v2.1/search?entity_id={}&entity_type={}&start={}".format(entity_id,entity_type,num)
	r1=get_request(url,key)
	if r1.status_code == 200:
		doc = r1.json()		
		if num == 0:
			num_res=doc['results_found']
			print('{} tiene {} restaurantes.\n'.format(city_name,num_res))
		for restaurant in doc['restaurants']:
			print('-->',restaurant['restaurant']['name'])