#!/usr/bin/python3

import urllib.parse
import os
import glob
import datetime
import json
import time

import sys
sys.path.append("../api")
import elasticsearch
sys.path.append("../www/scripts")
import maas_conf


def delete_indices ():
  x = elasticsearch.delete_index(es,"maas_config_fragments")
  x = elasticsearch.delete_index(es,"maas_config_entity_publish")
  x = elasticsearch.delete_index(es,"maas_config_entity_require")
  x = elasticsearch.delete_index(es,"maas_config_alert")
  x = elasticsearch.delete_index(es,"maas_alert_log_current")
  x = elasticsearch.delete_index(es,"maas_alert_log_history")
  x = elasticsearch.delete_index(es,"maas_entity_log_config")

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
  x = elasticsearch.create_index(es,"maas_entity_log_config",settings)
  x = elasticsearch.show_indices(es)
  for a in x:
    print(a.decode("UTF-8").rstrip())

es = { "url" : maas_conf.conf['elastic']['url'], "user" : maas_conf.conf['elastic']['user'], "pass" : maas_conf.conf['elastic']['pass'] }

#delete_indices()
time.sleep(2)
create_indices()
