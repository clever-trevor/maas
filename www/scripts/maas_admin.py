#!/usr/bin/python3

# This module runs some back end admin commands.
# 

import os
from urllib.request import Request,urlopen
import json
import maas_conf

# Common routine to execute the command and capture results
def run_cmd(command):
  try :
    result = os.popen(command)
    output = result.read().replace("\n","<BR>")
    content += "Executed " + command + "<BR>"
    content += "Results<BR><font face=courier>" + output
  except:
    content += "Error running " + command

  return

# Parse the command to be run and any other params
def admin(args):
  try:
    cmd = args['cmd']
  except:
    return "cmd is a mandatory parameter"
  # We must have a parameter called "admin" (This is a fake token!)
  try:
    admin = args['admin']
  except:
    return "Unauthorised"

  # Get the API URL in case we want to delete anything from the 
  # Database and/or Elastic instance 
  api_url = maas_conf.conf['api']['url']

  content = "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1>Monitoring Admin Tasks</h1>"
  content += "<hr>"

  # Delete metrics from InfluxDB
  if cmd == "delete-metrics" :
    if 'entity' in args:
      command = maas_conf.conf['influxdb']['binary'] + ' -database "telegraf" -execute "DROP SERIES WHERE host=\'%s\'"' % ( fs['entity'].value)
      run_cmd(command)

  # Delete all instances of an endpoint from Elastic via the API
  elif cmd == "delete-entity" :
    # usage : ?cmd=delete-entity&entity=<xxx>&admin=admin
    if 'entity' in args:
      entity = args['entity']
      params = { "entity" : entity, "admin":admin }
      data = str(json.dumps(params)).encode("utf-8")
      req = Request(api_url + "/admin/delete_entity",data=data)
      req.add_header('Content-Type','application/json')
      resp = str(urlopen(req).read(),'utf-8')
      content += "Delete Entity results below <BR>"
      content += resp

  else : 
    f = open(maas_conf.conf['maas']['base_dir'] + "/www/html/admin","r")
    content += f.read()

  return content
