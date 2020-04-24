#
import flask
from flask import request, jsonify
import elasticsearch
import influx
import configparser
import urllib.request
import socket
import datetime
import json

maas = configparser.RawConfigParser()
maas.read('/app/maas/conf/env')

es = { "url":maas['elastic']['url'], "user":maas['elastic']['user'], "pass":maas['elastic']['pass'] }
# Index names
config_entity_require = "maas_config_entity_require"
config_entity_publish = "maas_config_entity_publish"
config_alert = "maas_config_alert"
config_fragment = "maas_config_fragments"
log_alert_current = "maas_alert_log_current"
log_alert_history = "maas_alert_log_history"


influx_url = maas['influxdb']['url'] + "/query"

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.

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
@app.route('/api/v1/entity', methods=['GET'])
def api_get_entities():
    entity = "*"
    if 'entity' in request.args:
      entity = request.args['entity']

    try :
      x = elasticsearch.run_search_uri(es,config_entity_publish,"q=entity:" + entity + "&size=10000&_source_includes=entity,platform,last_updated")['hits']
      records = x['hits']
      json_string = "["
      for record in records:
        record = record['_source']
        json_string += '{"entity":"%s","platform":"%s","last_updated":"%s"},' % (record['entity'],record['platform'],record['last_updated'])
      json_string = json_string[:-1]
      json_string += "]"
    except :
      json_string = "{}"

    return jsonify(json_string)


################################################################################
# Entity based calls
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
        response = urllib.request.urlopen(maas['maas']['url'] + "/cgi-bin/telegraf-configure?host=" + entity)
        config = response.read()
      except:
        config = ""
      return config
    # Custom configuration only
    else:
      try:
        entity = request.args['entity']
      except:
        entity = "*"
      # Get the custom config from Elasticsearch
      try :
        x = elasticsearch.run_search_uri(es,config_entity_require,"q=entity.keyword:" + entity + "&size=10000")['hits']
        records = x['hits']

        json_string = "["
        for record in records:
          r = record['_source']
          json_string += '{"entity":"%s","platform":"%s","config":"%s","last_updated":"%s"},' % (r['entity'],r['platform'],r['config'],r['last_updated'])
        json_string = json_string[:-1]
        json_string += ']'

      except :
        json_string = "{}"

    return jsonify(json_string)

  ################### POST NEW CUSTOM CONFIG #########################
  elif request.method == 'POST' :
    data = request.get_json()
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

    now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
    doc = {"entity":entity,"config":config,"platform":platform,"last_updated":now}

    x = elasticsearch.post_document(es,config_entity_require,"_doc",entity,doc)
    return "200"


################################################################################
# Config Fragment based calls
# GET
#  /api/v1/config/fragment?name=
#   
@app.route('/api/v1/config/fragment', methods=['GET'])
def api_get_fragment():
  try:
    name = request.args['name']
  except:
    name = "*"

  try :
    x = elasticsearch.run_search_uri(es,config_fragment,"q=_id:" + name + "&size=10000")['hits']
    records = x['hits']
    if name != "*" :
      try:
        records = records[0]['_source']
      except:
        records = {}
  except :
    records = {}
  return jsonify(records)
  


################################################################################A
# Alert config calls
# GET
#  /api/v1/config/alert          Return all alert configurations
#  /api/v1/config/alert?entity=  Return alerts only for entity specified
#   
@app.route('/api/v1/config/alert', methods=['GET','POST','DELETE'])
def api_get_alert():
  #---------------- GET ----------------------#
  if request.method == 'GET' :
    try:
      entity = request.args['entity']
    except:
      entity = "*"

    try :
      x = elasticsearch.run_search_uri(es,config_alert,"q=entity.keyword:" + entity + "&size=10000")['hits']
      records = x['hits']
      json_string = "["
      for r in records:
        json_string += json.dumps(r['_source'])+ ","
      json_string = json_string[:-1] + "]"
    except :
      json_string = "[]"
  
    return jsonify(json_string)
 
  #---------------- POST ----------------------#
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

    key = "%s:%s:%s:%s:%s" % ( entity,metric_class,metric_object,metric_instance,metric_name )
    key = key.replace("/","%2F")

    now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

    doc = { "entity":entity, "metric_class":metric_class, "metric_object":metric_object, "metric_instance":metric_instance, "metric_name":metric_name, "alert_operator":alert_operator, "alert_threshold":alert_threshold, "support_team":support_team, "alert_tag":alert_tag, "last_updated":now }

    x = elasticsearch.post_document(es,config_alert,"_doc",key,doc)['result']

    return x

  #---------------- DELETE ----------------------#
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

    return x

################################################################################A
# Metric calls
################################################################################A
# GET
#  /api/v1/metric/last  Get last value for a given metric
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
    if metric_instance == "" :
      query="SELECT last(%s) from telegraf.autogen.%s WHERE host = '%s' " % (metric_name,metric_class,entity)
    else :
      query="SELECT last(%s) from telegraf.autogen.%s WHERE host = '%s' AND %s='%s'" % (metric_name,metric_class,entity,metric_object,metric_instance)
    value, time_stamp = influx.get_metric(influx_url,query)
  except:
    value = "0"
    time_stamp = "NA"

  return "{} {}".format(value,time_stamp)
     

# POST
#  /api/v1/metric   Post a new metric
#    entity=
#    metric_name=
#    metric_value=
#    app_id=
@app.route('/api/v1/metric/post', methods=['POST'])
def api_post_metric():
  try:
    entity = request.args['entity']
  except:
    return("entity is a mandatory field")

  try:
    app_id = request.args['app_id']
  except:
    return("app_id is a mandatory field")

  try:
    metric_name = request.args['metric_name']
  except:
    return("metric_name is a mandatory field")

  try:
    metric_value = request.args['metric_value']
  except:
    return("metric_value is a mandatory field")

  string = "statsd,app_id=%s,host=%s,metric_name=%s:%s|c" % (app_id,entity,metric_name,metric_value)
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.sendto(bytes(string,"utf-8"), ("127.0.0.1",9125))

  query = "SELECT mean(value) FROM telegraf.autogen.statsd WHERE time > now() - 1h AND app_id = '%s' AND entity='%s' AND metric_name = '%s' GROUP BY time(:interval:) FILL(null)" % ( app_id,entity,metric_name)
  query = urllib.parse.quote(query)
  url = maas['chronograf']['url'] + "/sources/1/chronograf/data-explorer?query=" + query


  return str(url)

# POST
#  /api/v1/log/alert    Post a new metric
#   log     DEtermines whether to write to current or history log
@app.route('/api/v1/admin/clear_current_alert_log', methods=['POST'])
def api_clear_current_alert_log():
  data = request.get_json()
  try:
    admin = data['admin']
  except:
    return "unable to process"
  doc = { "query":{"match_all": {} } }
  x = elasticsearch.es_function(es,log_alert_current,"_delete_by_query?conflicts=proceed",doc,"POST")
  return x

# POST
#  /api/v1/log/alert    Post a new metric
#   log     DEtermines whether to write to current or history log
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

  now = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")

  doc = {"entity":entity,"metric_class":metric_class,"metric_object":metric_object,"metric_instance":metric_instance,"metric_name":metric_name,"alert_operator":alert_operator,"alert_threshold":alert_threshold,"support_team":support_team,"status":status,"timestamp":now,"actual":actual,"metric_timestamp":metric_timestamp,"url":url}

  if log == "current": 
    index = log_alert_current
  else:
    index = log_alert_history

  x = elasticsearch.post_document(es,index,"_doc","",doc)

  return x

app.run(host='0.0.0.0',port=9000)

