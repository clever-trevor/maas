#!/usr/bin/python3

# This script checks the status/availabilty of the MaaS platform components

from urllib.request import Request,urlopen
import json
import datetime
import maas_conf
import sys
import socket
import os 

# Routine to check if a TCP endpoint is available
def port_check(component,host,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
  try :
    result = sock.connect_ex((host, port))
    if result == 0 :
      status = "Online"
    else:
      status = "Offline"
  except:
    result = 999
    status = "Offline"
  content = "<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>" % ( component, host + ":" + str(port), status )
  return content

def check():
  # Set some variables from this
  api_url = maas_conf.conf['api']['url']

  content = "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1><A style='text-decoration:none' HREF='/'>Infra Health</a></h1>"
  content += "<TABLE class='blueTable'><TR><TH>Component</TH><TH>Target</TH><TH>Status</TH></TR>"


  # Check Elasticsearch
  server = maas_conf.conf['elastic']['url'].split("//")[1]
  parts = server.split(":")
  host = parts[0]
  port = int(parts[1])
  content += port_check("Elasticsearch",host,port )
 
  # Check API
  server = maas_conf.conf['api']['url'].split("//")[1]
  parts = server.split(":")
  host = parts[0]
  port = int(parts[1].split("/")[0])
  content += port_check("MaaS API",host,port )
  
  # Check Influx
  server = maas_conf.conf['influxdb']['url'].split("//")[1]
  parts = server.split(":")
  host = parts[0]
  port = int(parts[1].split("/")[0])
  content += port_check("InfluxDB",host,port )

  # Check Chronograf
  server = maas_conf.conf['chronograf']['url'].split("//")[1]
  parts = server.split(":")
  host = parts[0]
  port = int(parts[1].split("/")[0])
  content += port_check("Chronograf",host,port )

  # Check Grafana 
  server = maas_conf.conf['grafana']['url'].split("//")[1]
  parts = server.split(":")
  host = parts[0]
  port = int(parts[1])
  content += port_check("Grafana",host,port )

  # Check Kafka
  parts = maas_conf.conf['kafka']['broker'].split(":")
  host = parts[0]
  port = int(parts[1])
  content += port_check("Kafka",host,port )

  # Check Kafka to Influx Feeder
  status = "Not Running"
  for line in os.popen("ps ax | grep kafta_to_influx.py | grep -v grep"):
    pid = line.split()[0]
    status = "Running PID:" + pid

  content += "<TR><TD>%s</TD><TD>%s</TD><TD>%s</TD></TR>" % ( "Kafka to Influx Feed", "kafta_to_influx.py",status)

 
  content += "</TABLE>"
  return content

