#!/usr/bin/python3

# This web page is used to build a configuration for a Telegraf agent 
# based on a URL call with some params
# os=  The template to use.  "linux" or "windows" supported
# host=  The hostname. This should be short name in lower case
# reset=   Set to "true" to rebuild the configuration on startup
# tags=  A series of tags to deploy templated monitoring packs for known componenents

import datetime
import json
from urllib.request import Request,urlopen
import maas_conf
import re

def configure(args):
  api_url = maas_conf.conf['api']['url']

  message = ""
  content = ""

  # We need host passed in as a param so check this is here
  if 'host' in args:
    # Store the host param value
    entity = args['host']
    # Validate format 
    if not bool(re.match("^[a-z0-9\-]+$", entity)):
      return "Invalid hostname - must be a-z0-9\- only"

    message = entity
    platform = ""

    # If config already exists then load from Elastic and store
    try:
      req = Request(api_url + "/config/entity?entity=" + entity + "&mode=live")
      resp = json.load(urlopen(req))
      content = resp['content']
      platform = resp['platform']
      message += " Config already exists"
    except:
      pass

    # If no existing config was found *or* the "reset" param was found
    # then lets build a new config from scratch based on a default platform
    # template and then layering on any custom metrics
    if content == "" or 'reset' in args :

      # If an OS param was supplied, then use that template
      if 'os' in args:
        platform = args['os']

      if platform != "":
        template = "telegraf." + platform + ".template"
      # No OS param so use very basic config
      else :
        template = "telegraf.template"

      # Get the base config for this host
      # "content" will be built up based on information in incoming request
      req =  Request(api_url + "/config/fragment?name=" + template)
      entity_frag = json.load(urlopen(req))

      # Replace some of the variables to match our target endpoints
      content = entity_frag.replace("\\n","\n").replace("\\\"","\"").replace("%HOST%",entity)
      content = content.replace("%INFLUXDB%",maas_conf.conf['influxdb']['url'])
      content = content.replace("\\n","\n").replace("\\\"","\"").replace("%BROKER%",maas_conf.conf['kafka']['broker'])

      # Now see if there is any custom metrics to collect
      try : 
        req =  Request(api_url + "/config/entity?entity=" + entity + "&mode=custom")
        resp = json.loads(json.load(urlopen(req)),strict=False)
        resp = resp[0]['config']
        collect = resp.replace("\\n","\n").replace("\\\"","\"").split()
      except:
        collect = ""

      agent_target = ""
      # For each custom metric found, pull in the appropriate template
      # and replace the key variables with desired values
      try :
        for line in collect:
          monitor_type,instance = line.rstrip().split("=")
          x = ""
          # Process monitor. 
          if monitor_type == "process" :
            fragment = "procstat." + platform + ".template"
            req =  Request(api_url + "/config/fragment?name=" + fragment)
            x = json.load(urlopen(req))
            x = x.replace("\\n","\n").replace("\\\"","\"").replace("%PROCESS%",instance)
          # Filesystem monitor
          elif monitor_type == "filesystem":
            fragment = "disk." + platform + ".template"
            req =  Request(api_url + "/config/fragment?name=" + fragment)
            x = json.load(urlopen(req))
            x = x.replace("\\n","\n").replace("\\\"","\"").replace("%FILESYSTEM%",instance)
          # URL monitor
          elif monitor_type == "http":
            fragment = "http.template"
            req =  Request(api_url + "/config/fragment?name=" + fragment)
            x = json.load(urlopen(req))
            x = x.replace("\\n","\n").replace("\\\"","\"").replace("%URL%",instance)
          # statsd listener
          elif monitor_type == "statsd":
            fragment = "statsd." + platform + ".template"
            req =  Request(api_url + "/config/fragment?name=" + fragment)
            x = json.load(urlopen(req))
            x = x.replace("\\n","\n").replace("\\\"","\"").replace("%PORT%",instance)
          # Pre-populated template
          elif monitor_type == "template":
            fragment = "template." + instance + "." + platform + ".template"
            req =  Request(api_url + "/config/fragment?name=" + fragment)
            x = json.load(urlopen(req))
            x = x.replace("\\n","\n").replace("\\\"","\"")

          # Add the processed fragment to the overall config
          content += x

        collect.close()

      except:
        pass
    
      message += " New config generated"

    # Now we have a complete config, let's write back to Elastic via API
    doc = {"entity":entity,"content":content,"platform":platform}
    data = str(json.dumps(doc)).encode('utf-8')
    req = Request(api_url + "/entity",data=data,method="POST")
    req.add_header('Content-Type','application/json')
    resp = str(urlopen(req).read(),'utf-8')

  else:
    message += " No hostname supplied"
    entity = "unknown"

  # Write a log message showing when agent last requested config
  doc = {"entity":entity,"message":message}
  data = str(json.dumps(doc)).encode('utf-8')
  req = Request(api_url + "/log/entity",data=data,method="POST")
  req.add_header('Content-Type','application/json')
  resp = urlopen(req).read()

  # And finally, print the config to the agent 
  return(content)

