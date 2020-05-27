#!/usr/bin/python3 

# This is a simple form where someone can either post a dummy metric via
# a web form, or if they prefer, can call the web page directly with the
# fields passed as params so that it can be done programatically

import urllib.parse
from urllib.request import Request,urlopen
import json
import maas_conf


# Data was passed into this page so let's check it and if valid,
# pass to Influx via the API
def post_metric(form):

  api_url = maas_conf.conf['api']['url']

  content = "<html><head><link rel='stylesheet' type='text/css' href='/static/dark.css'></head>"
  content += "<h1><A style='text-decoration:none' HREF='/'>Generate Test Metrics</a></h1>"
  content += "<hr>"

  # Check key fields were set
  if 'entity' in form and 'metric_name' in form and 'metric' in form and 'app_id' in form :
    try:
      app_id = form['app_id']
      entity = form['entity']
      metric_name = form['metric_name']
      metric_value = form['metric']

      # Build the document for this metric
      doc = { "entity":entity, "metric_name":metric_name, "metric_value":metric_value,"app_id":app_id }
      data = str(json.dumps(doc)).encode("utf-8")
      # Post to Influx
      req = Request(api_url + "/metric/post",data=data)
      req.add_header('Content-Type','application/json')
      url = str(urlopen(req).read(),'utf-8')

      content += "<h4>Metric Generated!</h4>"
  
      content += "<h4><A HREF='%s'>View the metric here</A></H4>" % (url) 
      content += "<h5>Please wait up to 1 minute for metric to appear!</h5>"
    except:
      content += "<h4>Problem generating metric - please check inputs"

  else :
    # Nothing was passed in so present a form where the user can
    # enter their own values before submitting
    content += "<h2>Enter your custom metric details below</h2>"
    content += """
<html>
<div align="center">
<FORM ACTION="/post-metric?mode=generate" METHOD="POST">
<TABLE>

 <TR>
  <TD>App Id (Numeric Only)</TD>
  <TD>
    <input name="app_id" id="app_id" pattern="[0-9]+"></input>
  </TD>
 </TR>

 <TR>
  <TD>Host Name (Lower Case)</TD>
  <TD>
    <input name="entity" id="entity" pattern="[a-z0-9\-]+"></input>
  </TD>
 </TR>

 <TR>
  <TD>Metric Name (a-z 0-9 _ -)</TD>
  <TD>
    <input name="metric_name" id="metric_name" pattern="[a-z0-9\_\-]+"></input>
  </TD>
 </TR>

 <TR>
  <TD>Metric Value (Numeric only)</TD>
  <TD>
    <input name="metric" id="metric" pattern="[0-9\.]+"></input>
  </TD>
 </TR>

 <TR>
  <TD COLSPAN=2 ALIGN=CENTER>
   <input type="submit"></input>
  </TD>
 </TR>

</TABLE>
</div>

</FORM>
"""


  return content
