#!/usr/bin/python3

import urllib.parse
from urllib.request import Request,urlopen
import json
import time
import datetime
import elasticsearch
import configparser
import influx

maas = configparser.RawConfigParser()
maas.read('/app/maas/conf/env')

def parse_alert_conf(conf_file):
  x = elasticsearch.run_search_uri(es,alert_config_index,"q=*&size=10000")['hits']
  records = x['hits']
  tests = 0
  for r in records:
    r = r['_source']
    host = r['host']
    metric_type = r['type']
    instance_name = r['instance_name']
    instance_value = r['instance_value']
    metric = r['metric']
    operator = r['operator']
    threshold = r['threshold']
    queue = r['queue']

    doc = {"host":host,"metric_type":metric_type,"instance_name":instance_name,"instance_value":instance_value,"metric":metric,"operator":operator,"threshold":threshold,"queue":queue}
    if metric_type == "disk" and instance_name == "path" and ":" in instance_value :
      instance_value = '\\\\' + instance_value

    # Now test this
    status = test_metric(host,metric_type,instance_name,instance_value,metric,operator,threshold)
    doc['status'] = status

    logMsg(log_current,doc)

    if "ALERT" in status:
      time_stamp = status.split()[2].split(":",1)[1]
      query = "SELECT %s FROM telegraf.autogen.%s WHERE time > \'%s\' -1h AND time < \'%s\' + 1h AND host = \'%s\' AND %s = \'%s\'" % ( metric,metric_type,time_stamp,time_stamp,host,instance_name,instance_value )
      query = urllib.parse.quote(query)
      url = maas['chronograf']['url'] + "/sources/1/chronograf/data-explorer?query=" + query
      doc['url'] = url
      escalate_alert(doc,url)

    tests += 1

  return tests

def escalate_alert(doc,url):
  logMsg(alert_history,doc)
  return

def test_metric(host,metric_type,instance_name,instance_value,metric,operator,threshold) :

  query="SELECT last(%s) from telegraf.autogen.%s WHERE host = '%s' AND %s='%s'" % (metric,metric_type,host,instance_name,instance_value) 
  value, time_stamp = influx.get_metric(influx_url,query)
  result = influx.test_metric(value,operator,threshold)

  if time_stamp == "" : 
      status = "NO-DATA-RETURNED"
  elif result == True :
    status = "ALERT : Actual:%s TimeSample:%s" % (value, time_stamp)
  else :
    status = "PASS : Actual:%s TimeSample:%s" % (value, time_stamp)

  return status

def logMsg(index,doc) :
  now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  doc['timestamp'] = now
  elasticsearch.post_document(es,index,"_doc","",doc)

def main():
  conf_file = "/app/influx/conf/alert.conf"
  tests = parse_alert_conf(conf_file)
  return tests

log_current = "maas_alert_log_current"
alert_history = "maas_alert_log_history"
alert_config_index = "maas_config_alert"
# Set Elasticsearch object
es = { "url": maas['elastic']['url'] ,"user": maas['elastic']['user'],"pass": maas['elastic']['pass'] }

# Delete old records from the "current" log
doc = { "query":{"match_all": {} } }
x = elasticsearch.es_function(es,log_current,"_delete_by_query?conflicts=proceed",doc,"POST")

influx_url = maas['influxdb']['url'] + "/query"
start = time.process_time()

tests = str(main())

time_taken = str(time.process_time() - start)
doc = { "host":"summary", "summary" : "Tests:" + tests + " Time Taken:" + time_taken}
logMsg(log_current,doc)
