#!/usr/bin/python3

import urllib.parse
import os
import glob
import datetime
import json
import elasticsearch
import configparser
import time

maas = configparser.RawConfigParser()
maas.read('/app/maas/conf/env')

def put_fragment(filename) :
  conf = open(filename,"r")
  config = ""
  for line in conf :
    line = line.rstrip().replace("\"","\\\"") + "\\n"
    line = line.replace("\{","\\{").replace("\}","\\}")
    line = line.replace("'","'\\''")
    config += line
  name = os.path.basename(filename).rstrip()
  now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  doc = { "fragment":config, "created":now }
  result = elasticsearch.post_document(es,"maas_config_fragments","_doc",name,doc)
  print(name + " : " + result['result'])

def load_fragments():
  templates = glob.glob("/app/maas/conf/fragments/*template")
  for template in templates:
    put_fragment(template)

es = { "url" : maas['elastic']['url'], "user" : maas['elastic']['user'], "pass" : maas['elastic']['pass'] }

load_fragments()

