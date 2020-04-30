#!/usr/bin/python3
#
import flask
from flask import request, jsonify
import elasticsearch
import influx
import urllib.request
import socket
import datetime
import json

import sys
sys.path.append("../www/scripts")
import maas_conf

# Elasticsearch object
es = { "url":maas_conf.conf['elastic']['url'], "user":maas_conf.conf['elastic']['user'], "pass":maas_conf.conf['elastic']['pass'] }

# Index names
config_entity_require = "maas_config_entity_require"
config_entity_publish = "maas_config_entity_publish"
config_alert = "maas_config_alert"
config_fragment = "maas_config_fragments"
log_alert_current = "maas_alert_log_current"
log_alert_history = "maas_alert_log_history"
log_config = "maas_entity_log_config"

# Influx API
influx_url = maas_conf.conf['influxdb']['url'] + "/query"

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Home page - do nothing
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Metrics as a Service API</h1>
<p>A prototype API for the Metrics as a Service platform</p>'''


################################################################################
# Entity inventory and data
# GET
#  /api/v1/entity           Return all entities which have connected at least once
#  /api/v1/entity?entity=   Return only the entity specified in the query
#   
@app.route('/api/v1/entity', methods=['GET','POST'])
def api_get_entities():
  # GEt details about an entity
  if request.method == "GET" :
    # Show all hosts if a param was not provided
    entity = "*"
    if 'entity' in request.args:
      entity = request.args['entity']

    # Query Elastic and get results
    try :
      # Look at the index which contains all hosts that have called in
      x = elasticsearch.run_search_uri(es,config_entity_publish,"entity:" + entity,"&size=10000&_source_includes=entity,platform,last_updated")['hits']
      records = x['hits']
      json_string = "["
      # Parse through all records and build a new output structure
      for record in records:
        record = record['_source']
        json_string += '{"entity":"%s","platform":"%s","last_updated":"%s"},' % (record['entity'],record['platform'],record['last_updated'])
      json_string = json_string[:-1]
      json_string += "]"
    except :
      # Bad query or exception so return nothing
      json_string = "{}"

    return jsonify(json_string)

  # Update details for an entity
  elif request.method == "POST" :
    data = request.get_json()
    # Test some mandatory fields
    try:
      entity = data['entity']
    except:
      return "entity is a mandatory field"
    try:
      content = data['content']
    except:
      return "content is a mandatory field"
    try:
      platform = data['platform']
    except:
      return "platform is a mandatory field"

    # Add or Update the entry
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    doc = {"entity":entity,"content":content,"last_updated":now,"platform":platform}
    x = elasticsearch.post_document(es,config_entity_publish,"_doc",entity,doc)['result']
    return x



################################################################################
# Entity config based calls
# GET
#  /api/v1/config/entity?entity=xx&mode=(custom|full)
#    mode=custom   Return only additional configuration for the specified entitiy
#    mode=live     Return the live (full) configuration for the specified entitiy
# POST
#  /api/v1/config/entity?entity=xx&config=xx&platform=xx
#  Post a new configuration
#  

@app.route('/api/v1/config/entity', methods=['GET','POST'])
def api_get_config():

  ################### GET EXISTING CUSTOM CONFIG #########################
  if request.method == 'GET' : 
    # Test to see if mode was supplied, otherwise default to "live"
    try:
      mode = request.args['mode']
    except :
      mode = "live"

    # Full mode means get full Telegraf config
    if mode == "live":
      # Entity is a mandated field
      try:
        entity = request.args['entity']
      except:
        return("entity field missing")
  
      # Collect the live config from the entity (Same as agent requests on startup)
      try:
        config = elasticsearch.run_search_uri(es,config_entity_publish,"entity.keyword:" + entity,"&size=10000")['hits']
        config = config['hits'][0]['_source']
      except:
        config = ""
      return jsonify(config)

    # Custom configuration only which is product agnostic
    else:
      try:
        entity = request.args['entity']
      except:
        entity = "*"
      # Get the custom config from Elasticsearch
      try :
        x = elasticsearch.run_search_uri(es,config_entity_require,"entity.keyword:" + entity,"&size=10000")['hits']
        records = x['hits']

        # Build a new json structure 
        json_string = "["
        for record in records:
          r = record['_source']
          json_string += '{"entity":"%s","platform":"%s","config":"%s","last_updated":"%s"},' % (r['entity'],r['platform'],r['config'],r['last_updated'])
        json_string = json_string[:-1]
        json_string += ']'

      except :
        json_string = "{}"

    # REturn whatever we found
    return jsonify(json_string)

  ################### POST NEW CUSTOM CONFIG #########################
  elif request.method == 'POST' :
    # REad in the "data" from the post request
    data = request.get_json()
    # Check out mandatory params
    try:
      entity = data['entity']
    except:
      return("entity is a mandatory parameter")
    try:
      platform = data['platform']
    except:
      return("platform is a mandatory parameter")
    try:
      config = data['config']
    except:
      return("config is a mandatory parameter")

    # Build new config document and post it
    now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    doc = {"entity":entity,"config":config,"platform":platform,"last_updated":now}
    x = elasticsearch.post_document(es,config_entity_require,"_doc",entity,doc)['result']
    return x


################################################################################
# Config Fragment based calls.  Used to retrieve template fragemtns
# GET
#  /api/v1/config/fragment?name=
#   
@app.route('/api/v1/config/fragment', methods=['GET'])
def api_get_fragment():
  # If "name" of fragement passed, return only that one otherwise
  # return JSON array of all fragements
  try:
    name = request.args['name']
  except:
    name = "*"

  try :
    x = elasticsearch.run_search_uri(es,config_fragment,"_id:" + name, "&size=10000")['hits']
    records = x['hits']
    # We specified a single fragement so return the config portion only
    if name != "*" :
      try:
        records = records[0]['_source']['fragment']
      except:
        records = {}
  except :
    records = {}
  return jsonify(records)
  

###############################################################################
# Get a list of all tags found in the alerts config
# GET
#   /api/v1/config/alert/tags

@app.route('/api/v1/config/alert/tags', methods=['GET'])
def api_get_alert_tags():
  # There could be lots of alert definitions fo aggregate the alert_tag
  # field to make processing quicker
  query = {"size":0,"aggs":{"uniq_alert_tags":{"terms":{"field":"alert_tag.keyword"}}}}
  x = elasticsearch.run_search(es,config_alert,query)['aggregations']['uniq_alert_tags']['buckets']
  # Build a JSON array with each term found
  json_string =  "["
  for alert_tag in x:
    json_string += '{"tag":"%s"},' % ( alert_tag['key'] )
  json_string = json_string[:-1] + "]"
  return jsonify(json_string)


###############################################################################
# Alert config calls
# GET
#  /api/v1/config/alert          Return all alert configurations
#  /api/v1/config/alert?entity=  Return alerts only for entity specified
#   
@app.route('/api/v1/config/alert', methods=['GET','POST','DELETE'])
def api_get_alert():
  #---------------- GET ----------------------#
  # Get the definition of an existing alert config
  if request.method == 'GET' :
    try:
      entity = request.args['entity']
    except:
      entity = "*"
    try:
      alert_tag = "*" + request.args['alert_tag'] + "*"
    except:
      alert_tag = "*"
    try :
      query = "entity.keyword:" + entity + " AND alert_tag:" + alert_tag 
      x = elasticsearch.run_search_uri(es,config_alert,query,"&size=10000")['hits']
      records = x['hits']
      json_string = "["
      x = 0
      for r in records:
        x = x + 1
        json_string += json.dumps(r['_source']) + ","
      json_string = json_string[:-1] 
      json_string += "]"
    except :
      json_string = "[]"

    return jsonify(json_string)
 
  #---------------- POST ----------------------#
  # Add a new alert definition (or update an existing one)
  elif request.method == 'POST' :
    data = request.get_json()
    try:
      entity = data['entity']
    except:
      return("entity is a mandatory parameter")
    try:
      metric_class = data['metric_class']
    except:
      return("metric_class is a mandatory parameter")
    try:
      metric_object = data['metric_object']
    except:
      return("metric_object is a mandatory parameter")
    try:
      metric_instance = data['metric_instance']
    except:
      return("metric_instance is a mandatory parameter")
    try:
      metric_name = data['metric_name']
    except:
      return("metric_name is a mandatory parameter")
    try:
      alert_operator = data['alert_operator']
    except:
      return("alert_operator is a mandatory parameter")
    try:
      alert_threshold = data['alert_threshold']
    except:
      return("alert_threshold is a mandatory parameter")
    try:
      support_team = data['support_team']
    except:
      return("support_team is a mandatory parameter")
    try:
      alert_tag = data['alert_tag']
    except:
      alert_tag = ""

    # BUild a key so that we only have one alert defined for each metric 
    key = "%s:%s:%s:%s:%s" % ( entity,metric_class,metric_object,metric_instance,metric_name )
    key = key.replace("/","%2F")

    # Post the alert
    now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    doc = { "entity":entity, "metric_class":metric_class, "metric_object":metric_object, "metric_instance":metric_instance, "metric_name":metric_name, "alert_operator":alert_operator, "alert_threshold":alert_threshold, "support_team":support_team, "alert_tag":alert_tag, "last_updated":now }
    x = elasticsearch.post_document(es,config_alert,"_doc",key,doc)['result']

    return x

  #---------------- DELETE ----------------------#
  # Delete an existing alert config based on key name
  elif request.method == 'DELETE' :
    data = request.get_json()
    try:
      entity = data['entity']
    except:
      return "entity is a mandatory field"
    try:
      metric_class = data['metric_class']
    except:
      return("metric_class is a mandatory parameter")
    try:
      metric_object = data['metric_object']
    except:
      return("metric_object is a mandatory parameter")
    try:
      metric_instance = data['metric_instance']
    except:
      return("metric_instance is a mandatory parameter")
    try:
      metric_name = data['metric_name']
    except:
      return("metric_name is a mandatory parameter")
 
    try:
      key = "%s:%s:%s:%s:%s" % ( entity,metric_class,metric_object,metric_instance,metric_name )
      x = elasticsearch.delete_document_by_id(es,config_alert,"_doc",key)['result']
    except:
      x = "no valid key match"

    if x == "deleted":
      now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
      # TODO : Log message here

    return x

################################################################################
# Metric calls
################################################################################
# GET
#  /api/v1/metric/last  Get last value for a given metric
#    Get last value of a metric from Influx
#    entity=
#    metric_class=
#    metric_name=
#    metric_object=
#    metric_instance=
@app.route('/api/v1/metric/last', methods=['GET'])
def api_get_metric_last():
  try:
    entity = request.args['entity']
  except:
    return("entity is a mandatory field")
  try:
    metric_class = request.args['metric_class']
  except:
    return("metric_class is a mandatory parameter")
  try:
    metric_object = request.args['metric_object']
  except:
    metric_object = ""
  try:
    metric_instance = request.args['metric_instance']
  except:
    metric_instance = ""
  try:
    metric_name = request.args['metric_name']
  except:
    return("metric_name is a mandatory parameter")

  try:
    # Build the INflux query string depending on what params were passed ni
    if metric_instance == "" :
      query="SELECT last(%s) from telegraf.autogen.%s WHERE host = '%s' " % (metric_name,metric_class,entity)
    else :
      query="SELECT last(%s) from telegraf.autogen.%s WHERE host = '%s' AND %s='%s'" % (metric_name,metric_class,entity,metric_object,metric_instance)
    value, time_stamp = influx.get_metric(influx_url,query)
  except:
    # The query didn't work do set some defaults
    value = "0"
    time_stamp = "NA"

  return "{} {}".format(value,time_stamp)
     

###############################################################
# POST
#  /api/v1/metric   Post a new metric
#    entity=
#    metric_name=
#    metric_value=
#    app_id=
@app.route('/api/v1/metric/post', methods=['POST'])
def api_post_metric():
  data = request.get_json()

  try:
    entity = data['entity']
  except:
    return("entity is a mandatory field")
  try:
    app_id = data['app_id']
  except:
    return("app_id is a mandatory field")
  try:
    metric_name = data['metric_name']
  except:
    return("metric_name is a mandatory field")
  try:
    metric_value = data['metric_value']
  except:
    return("metric_value is a mandatory field")

  # WE're hacking this a little bit by using statsd listener which 
  # Telegraf will poll.  It's quick but would be need to be enhanced
  # over time
  string = "statsd,app_id=%s,host=%s,metric_name=%s:%s|c" % (app_id,entity,metric_name,metric_value)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(bytes(string,"utf-8"), ("127.0.0.1",9500))
 
  # Build a URL which the user would be able to jump to see the data
  query = "SELECT mean(value) FROM telegraf.autogen.statsd WHERE time > now() - 1h AND app_id = '%s' AND entity='%s' AND metric_name = '%s' GROUP BY time(:interval:) FILL(null)" % ( app_id,entity,metric_name)
  query = urllib.parse.quote(query)
  url = maas_conf.conf['chronograf']['url'] + "/sources/1/chronograf/data-explorer?query=" + query

  return str(url)

#########################################################################
# Admin functions
########################################################################
# POST
#   /api/v1/admin/clear_current_alert_log 
#    Delete all documents from the "Alert Current" history log
@app.route('/api/v1/admin/clear_current_alert_log', methods=['POST'])
def api_clear_current_alert_log():
  data = request.get_json()
  # Check our "admin" token ;)
  try:
    admin = data['admin']
  except:
    return "unable to process"
  # Elastic query to match all docs
  doc = { "query":{"match_all": {} } }
  # And run a delete using this query
  x = elasticsearch.es_function(es,log_alert_current,"_delete_by_query?conflicts=proceed",doc,"POST")
  return x

# POST
#   /api/v1/admin/clear_current_alert_log  Removes all documents from index
#    DElete an entity from all places it resides in (not metrics though)
@app.route('/api/v1/admin/delete_entity', methods=['POST'])
def api_delete_entity():
  data = request.get_json()
  try:
    admin = data['admin']
  except:
    return "unable to process"
  try : 
    entity = data['entity']
  except :
    return "no entity passed"

  # Build a query to match this host
  doc = { "query":{"match": {"entity":entity } } }
  # String to caputre all output 
  results = ""
  x = elasticsearch.es_function(es,config_entity_require,"_delete_by_query?conflicts=proceed",doc,"POST")
  results = "entity-require:" + str(x) + "<BR>"
  x = elasticsearch.es_function(es,config_entity_publish,"_delete_by_query?conflicts=proceed",doc,"POST")
  results += "entity-publish:" + str(x) + "<BR>"
  x = elasticsearch.es_function(es,config_alert,"_delete_by_query?conflicts=proceed",doc,"POST")
  results += "config-alert-publish:" + str(x) + "<BR>"
  # Return the output
  return results


#######################################################################
# Logging Functions
#######################################################################
# POST
#  /api/v1/log/entity   Logs a message whenever a host connects
#   
@app.route('/api/v1/log/entity', methods=['POST'])
def api_log_entity():
  data = request.get_json()

  try:
    entity = data['entity']
  except:
    return("entity is a mandatory parameter")
  try:
    message = data['message']
  except:
    return("message is a mandatory parameter")

  # Log message that a host connected
  now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
  doc = { "entity":entity, "message":message, "timestamp":now} 
  x = elasticsearch.post_document(es,log_config,"_doc","",doc)['result']
  return x


# POST
#  /api/v1/log/alert    Post a new metric
#   log     Determines whether to write to current or history log
@app.route('/api/v1/log/alert', methods=['POST'])
def api_log_alert():
  data = request.get_json()
  try:
    log = data['log']
  except:
    return("log is a mandatory parameter")
  try:
    entity = data['entity']
  except:
    return("entity is a mandatory parameter")
  try:
    metric_class = data['metric_class']
  except:
    return("metric_class is a mandatory parameter")
  try:
    metric_object = data['metric_object']
  except:
    return("metric_object is a mandatory parameter")
  try:
    metric_instance = data['metric_instance']
  except:
    return("metric_instance is a mandatory parameter")
  try:
    metric_name = data['metric_name']
  except:
    return("metric_name is a mandatory parameter")
  try:
    alert_operator = data['alert_operator']
  except:
    return("alert_operator is a mandatory parameter")
  try:
    alert_threshold = data['alert_threshold']
  except:
    return("alert_threshold is a mandatory parameter")
  try:
    support_team = data['support_team']
  except:
    return("support_team is a mandatory parameter")
  try:
    status = data['status']
  except:
    return("status is a mandatory parameter")
  try:
    actual = data['actual']
  except:
    return("actual is a mandatory parameter")
  try:
    metric_timestamp = data['metric_timestamp']
  except:
    return("metric_timestamp is a mandatory parameter")
  try:
    url = data['url']
  except:
    return("url is a mandatory parameter")

  # Build message for alert breach
  now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
  doc = {"entity":entity,"metric_class":metric_class,"metric_object":metric_object,"metric_instance":metric_instance,"metric_name":metric_name,"alert_operator":alert_operator,"alert_threshold":alert_threshold,"support_team":support_team,"status":status,"timestamp":now,"actual":actual,"metric_timestamp":metric_timestamp,"url":url}

  # DEtemine if this is a current log or history
  if log == "current": 
    index = log_alert_current
  else:
    index = log_alert_history

  x = elasticsearch.post_document(es,index,"_doc","",doc)

  return x

# Start the app and listen on all interfaces, port 9000
app.run(host='0.0.0.0',port=9000)

