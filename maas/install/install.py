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

def delete_indices ():
  x = elasticsearch.delete_index(es,"maas_config_fragments")
  x = elasticsearch.delete_index(es,"maas_config_entity_publish")
  x = elasticsearch.delete_index(es,"maas_config_entity_require")
  x = elasticsearch.delete_index(es,"maas_config_alert")
  x = elasticsearch.delete_index(es,"maas_alert_log_current")
  x = elasticsearch.delete_index(es,"maas_alert_log_history")
  x = elasticsearch.delete_index(es,"maas_agent_configure_log_history")

def create_indices ():
  settings = {"settings":{ "number_of_shards" : 1, "number_of_replicas":0 } }
  # Templates used to build up host configirations
  x = elasticsearch.create_index(es,"maas_config_fragments",settings)

  settings = {"settings":{ "number_of_shards" : 1, "number_of_replicas":0 }, "mappings":{ "properties":{"last_updated":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"}}}}
  # Fully populated config per host
  x = elasticsearch.create_index(es,"maas_config_entity_publish",settings)
  # Custom monitoring requirements
  x = elasticsearch.create_index(es,"maas_config_entity_require",settings)
  # Alert settings
  x = elasticsearch.create_index(es,"maas_config_alert",settings)

  settings = {"settings":{ "number_of_shards" : 1, "number_of_replicas":0 }, "mappings":{ "properties":{"timestamp":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"},"metric_timestamp":{"type":"date","format":"yyyy/MM/dd HH:mm:ss"}}}}
  # Latest results from alert run
  x = elasticsearch.create_index(es,"maas_alert_log_current",settings)
  # History of all alerts generated
  x = elasticsearch.create_index(es,"maas_alert_log_history",settings)

  # Log of incoming configuration requests
  settings = {"settings":{ "number_of_shards" : 1, "number_of_replicas":0 }, "mappings":{ "properties":{"timestamp":{"type":"date","format":"dd/MM/yyyy HH:mm:ss"}}}}
  x = elasticsearch.create_index(es,"maas_agent_configure_log_history",settings)
  x = elasticsearch.show_indices(es)
  for a in x:
    print(a.decode("UTF-8").rstrip())

def create_symlinks():
  os.popen("ln -s /app/maas/python/elasticsearch.py /app/maas/install/elasticsearch.py")
  
  os.popen("ln -s /app/maas/python/influx.py        /app/maas/api/influx.py")
  os.popen("ln -s /app/maas/python/elasticsearch.py /app/maas/api/elasticsearch.py")

  os.popen("ln -s /app/maas/python/elasticsearch.py /app/www/cgi-bin/elasticsearch.py")
  os.popen("ln -s /app/maas/python/influx.py        /app/www/cgi-bin/influx.py")
 
es = { "url" : maas['elastic']['url'], "user" : maas['elastic']['user'], "pass" : maas['elastic']['pass'] }

#delete_indices()
time.sleep(2)
create_indices()
create_symlinks()
