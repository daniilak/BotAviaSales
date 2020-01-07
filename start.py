import requests
import json
import gzip

with open("airports.json",encoding='utf-8', errors='ignore') as json_data:
     airports = json.load(json_data, strict=False)
     print(airports[0])
# exit()

token = '63a4eacdfde5ed547e87cfa50fd98a16'
token_vk = '12bf474b28c9fa22d1bd1869fe9eced08ab68088cc6aeb74627bef240f763f4ab375175078cc7af8ee5f7'
url = 'http://api.travelpayouts.com/v2/prices/latest?origin=KZN&currency=rub&period_type=year&page=1&limit=30&show_to_affiliates=true&sorting=price&token='+token
# http://api.travelpayouts.com/v1/prices/direct?origin=KZN&depart_date=2020-01-17&return_date=2020-01-19&token=63a4eacdfde5ed547e87cfa50fd98a16
custom_header = {'Accept-Encoding': 'gzip'}
response = requests.get(url, headers=custom_header)

loaded_json = json.loads(response.text)
if not loaded_json['success']:
    print("Error")

for x in loaded_json['data']:
    code_airport = ""
    for airport in airports:
        if airport['city_code'] == x['destination']:
            code_airport  = airport['name']
            break
    print("destination = {0}\n value = {1} руб.\n".format(code_airport , x['value']))