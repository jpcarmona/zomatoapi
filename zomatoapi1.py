# 1. Posibilitar buscar restaurantes en otra ciudad.

##-- bash> export key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

import requests
import os

key=os.environ["key"]
cabecera={"Accept": "application/json", "user-key": key  }

num=0
url1="https://developers.zomato.com/api/v2.1/search?entity_id=36932&entity_type=subzone&start="+str(num)
r1=requests.get(url1,headers=cabecera)

if r1.status_code == 200:
	doc = r1.json()
	num_res=doc['results_found']
	print('Nueva York tiene',num_res,'restaurantes.\n')
	for res in doc['restaurants']:
		print('-->',res['restaurant']['name'])

opcion=input("\nDesea seguir viendo restaurantes de Nueva York (s/si, n/no)\n")
while opcion=="s":
	num+=20
	url1="https://developers.zomato.com/api/v2.1/search?entity_id=36932&entity_type=subzone&start="+str(num)
	r1=requests.get(url1,headers=cabecera)
	
	if r1.status_code == 200:
		doc = r1.json()
		num_res=doc['results_found']
		for res in doc['restaurants']:
			print('-->',res['restaurant']['name'])
	
	opcion=input("\nDesea seguir viendo restaurantes de Nueva York (s/si, n/no)\n")