import os
from urllib.request import Request,urlopen
import json
import maas_conf

def run_cmd(command):
  try :
    result = os.popen(command)
    output = result.read().replace("\n","<BR>")
    content += "Executed " + command + "<BR>"
    content += "Results<BR><font face=courier>" + output
  except:
    content += "Error running " + command

  return

def admin(args):
  try:
    cmd = args['cmd']
  except:
    return "cmd is a mandatory parameter"
  try:
    admin = args['admin']
  except:
    return "Unauthorised"

  api_url = maas_conf.conf['api']['url']

  content = "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1>Monitoring Admin Tasks</h1>"
  content += "<hr>"

  if cmd == "delete-metrics" :
    if 'entity' in args:
      command = maas_conf.conf['influxdb']['binary'] + ' -database "telegraf" -execute "DROP SERIES WHERE host=\'%s\'"' % ( fs['entity'].value)
      run_cmd(command)

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
