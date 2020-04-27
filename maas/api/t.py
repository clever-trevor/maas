#!/usr/bin/python3
from urllib.request import Request,urlopen
import urllib.parse
import configparser
import json

maas = configparser.RawConfigParser()
maas.read('/app/maas/conf/env')

api_url = maas['api']['url']

req = Request(api_url + "/config/alert",method="GET")
alerts = json.loads(json.load(urlopen(req)))
print(alerts)

