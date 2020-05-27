#!/usr/bin/python3

# This module pulls out all alert configurations and tests each one
# If a threshold is breached, a log message is written to Elastic 
# and an "escalate" function called which will ultimately generate
# a "real" event so some downstream system

import urllib.parse
from urllib.request import Request,urlopen
import maas_utils
import json
import time
import datetime
import maas_conf
import maas_utils

api_url = maas_conf.conf['api']['url']

def html_header():
  global content
  content += "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1><A style='text-decoration:none' HREF='/'>Alert Evaluation</a></h1>"
  content += "<hr>"
  return content

def parse_alerts():
  global content
  content += " <TABLE class='blueTable'><TR><TH>Host<TH>Metric Class<TH>Metric Object<TH>Metric Instance<TH>Metric Name<TH>Alert Operator<TH>Alert Threshold<TH>Support Team<TH>Status<TH>Measured Value<TH>Metric Time</TR>"

  # Get all alert configurations via the API
  req = Request(api_url + "/config/alert",method='GET')
  records = json.loads(json.load(urlopen(req)))
  records = sorted(records,key=lambda i: i['entity'])

  # Some counters for summary view later on
  tests = 0
  passes = 0
  alerts = 0
  fails = 0

  # Now loop through and test each alert
  for r in records:
    entity = r['entity']
    metric_class = r['metric_class']
    metric_object = r['metric_object']
    metric_instance = r['metric_instance']
    metric_name = r['metric_name']
    alert_operator = r['alert_operator']
    alert_threshold = r['alert_threshold']
    support_team = r['support_team']

    # A hack for disk alert where Windows disks are represented as
    # Linux paths
    if metric_class == "disk" and metric_instance == "path" and ":" in metric_object :
      metric_object = '\\\\' + metric_object

    # Now test call the function to test this metric
    status,actual,metric_timestamp = test_metric(entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold)

    # Hard coded formatting at the moment just to make it look a 
    # little neater
    actual = "{:.2f}".format(actual)

    # Build a URL which links to the Chronograf dashboard at time of measurement
    query = "SELECT %s FROM telegraf.autogen.%s WHERE time > \'%s\' -1h AND time < \'%s\' + 1h AND host = \'%s\' " % ( metric_name,metric_class,metric_timestamp,metric_timestamp,entity)
    if metric_instance != "" and metric_instance != "NULL": 
      query += " AND %s = \'%s\'" % ( metric_instance,metric_object )
    query = urllib.parse.quote(query)
    url = maas_conf.conf['chronograf']['url'] + "/sources/1/chronograf/data-explorer?query=" + query

    # Log the results in the Elastic log
    logMsg("current",entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,status,actual,metric_timestamp,url)

    # Colour the cell dependant on result
    if "ALERT" in status:
      alerts += 1
      escalate_alert(entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,status,actual,metric_timestamp,url)
    elif "PASS" in status:
      passes += 1
    else :
      fails += 1
        
    if status == "PASS" :
      status = "<FONT COLOR=GREEN>%s</FONT>" % (status)
    else:
      status = "<FONT COLOR=RED>%s</FONT>" % (status)

    content += "<TR><TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s<TD>%s</TR>" % ( entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,status,actual,metric_timestamp) 

    tests += 1

  content += "</TABLE>"

  content += "<H3>%s Tests evaluated<BR>Passes=%s Alerts=%s Failed=%s</H3>" % ( tests, passes,alerts,fails)

  return tests

# This function is called when we want to escalate the alert.
def escalate_alert(entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,status,actual,metric_timestamp,url):
  logMsg("history",entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,status,actual,metric_timestamp,url)
  return

# Test the alert configuration against latest Influx data point
def test_metric(entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold) :
  params = "entity=%s&metric_class=%s&metric_object=%s&metric_instance=%s&metric_name=%s" % ( entity,metric_class,metric_object,metric_instance,metric_name)

  # Get last metric via API
  req = Request(api_url + "/metric/last?" + params,method='GET')
  value, metric_timestamp = str(urlopen(req).read(),'utf-8').split(' ')
  try:
    value = float(value)
  except:
    value = 0

  # Evaluate the actual vs threshold
  result = maas_utils.evaluate_metric(value,alert_operator,alert_threshold)
  metric_timestamp = metric_timestamp.replace("T"," ").replace("Z","")

  # If no metric data exists, mark as such
  if metric_timestamp == "" or metric_timestamp == "NULL":
      status = "NODATARETURNED"
      value = 0
      metric_timestamp = 0
  elif result == True :
    status = "ALERT"
  else :
    status = "PASS"

  return status,value,metric_timestamp

# Function to log a message to Elastic for each alert tested
def logMsg(index,entity,metric_class,metric_object,metric_instance,metric_name,alert_operator,alert_threshold,support_team,status,actual,metric_timestamp,url) :

  # Build the structured log message
  doc = { "log":index,"entity":entity, "metric_class":metric_class, "metric_object":metric_object, "metric_instance":metric_instance, "metric_name":metric_name, "alert_operator":alert_operator, "alert_threshold":alert_threshold, "support_team":support_team, "status":status,"actual":actual,"metric_timestamp":metric_timestamp,"url":url }
  data = str(json.dumps(doc)).encode("utf-8")

  # Sent to Elastic via API
  req = Request(api_url + "/log/alert",data=data)
  req.add_header('Content-Type','application/json')
  resp = str(urlopen(req).read(),'utf-8')

# Routine which wrappers the other functions to test alerts
def evaluate(args):
  global content
  content = ""
  api_url = maas_conf.conf['api']['url']
  # Delete old records from the "current" log
  doc = { "admin":"admin"}
  data = str(json.dumps(doc)).encode("utf-8")
  req = Request(api_url + "/admin/clear_current_alert_log",data=data)
  req.add_header('Content-Type','application/json')
  resp = str(urlopen(req).read(),'utf-8')

  start = time.process_time()

  html_header()
  tests = str(parse_alerts())

  time_taken = str(time.process_time() - start)
  summary = "Tests:" + tests + " Time Taken:" + time_taken
  logMsg("current","summary","","","","","","","",summary,"","","")
  content += "</html>"

  return content

