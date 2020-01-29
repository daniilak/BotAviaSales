# /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import requests
import json
import gzip
import vk
import peewee
import json
from requests import post
from config import AVIATOKEN
from lib.Requests import Requests
from Subs import Aviasales_subs, get_subs
from lib.DataBase import DataBase, IntegrityError, OperationalError

db = DataBase()
with open("json/airports.json", encoding='utf-8', errors='ignore') as json_data:
    airports = json.load(json_data, strict=False)

while True:
    try:
        try:
            db.open_connection()
        except (peewee.OperationalError):
            print("connection")
    except (IntegrityError, OperationalError):
        db = DataBase()
        db.open_connection()
    subs = get_subs()
    url = "http://api.travelpayouts.com/v1/prices/direct?origin={0}&depart_date={1}&return_date={2}&token={3}".format(subs.origin, subs.depart_date, subs.return_date, AVIATOKEN
                                                                                                                      )
    custom_header = {'Accept-Encoding': 'gzip'}
    response = requests.get(url, headers=custom_header)

    loaded_json = json.loads(response.text)
    if not loaded_json['success']:
        print("Error")

    for x in loaded_json['data']:
        code_airport = ""
        for airport in airports:
            if airport['city_code'] == x['destination']:
                code_airport = airport['name']
                break
        msg = ("destination = {0}\n value = {1} руб.\n".format(
            code_airport, x['value']))
    r = Requests(subs.user_id)
    r.send_msg(msg)
    db.close_connection()
