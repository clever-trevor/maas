#
import flask
from flask import request, jsonify
import elasticsearch
import configparser
import urllib.request
import socket

maas = configparser.RawConfigParser()
maas.read('/app/maas/conf/env')

es = { "url":maas['elastic']['url'], "user":maas['elastic']['user'], "pass":maas['elastic']['pass'] }
host_config_index_in = "maas_config_entity_require"
host_config_index_out = "maas_config_entity_publish"
alert_config = "maas_config_alert"
fragment_config = "maas_config_fragments"

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

    query = "*"
    if 'entity' in request.args:
      query = request.args['entity']

    try :
      x = elasticsearch.run_search_uri(es,host_config_index_out,"q=" + query + "&size=10000")['hits']
      records = x['hits']
    except :
      records = {}

    
    return jsonify(records)


################################################################################
# Entity based calls
# GET
#  /api/v1/config/entity?entity=xx&mode=(custom|full)
#    mode=custom   Return only additional configuration for the specified entitiy
#    mode=live     Return the live (full) configuration for the specified entitiy
#   
@app.route('/api/v1/config/entity', methods=['GET'])
def api_get_config():

    # Entity is a mandated field
    try:
      entity = request.args['entity']
    except:
      return("entity field missing")

    # Test to see if mode was supplied, otherwise default to "live"
    try:
      mode = request.args['mode']
    except :
      mode = "live"

    # Full mode means get full Telegraf config
    if mode == "live":
      # Collect the live config from the entity (Same as agent requests on startup)
      try:
        response = urllib.request.urlopen(maas['maas']['url'] + "/cgi-bin/telegraf-configure?host=" + entity)
        config = response.read()
      except:
        config = ""
      return config
    # Custom configuration only
    else:
      # Get the custom config from Elasticsearch
      try :
        x = elasticsearch.run_search_uri(es,host_config_index_in,"q=entity.keyword:" + entity + "&size=10000")['hits']
        records = x['hits'][0]['_source']
      except :
        records = {}

    return jsonify(records)


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
    x = elasticsearch.run_search_uri(es,fragment_config,"q=_id:" + name + "&size=10000")['hits']
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
@app.route('/api/v1/config/alert', methods=['GET'])
def api_get_alert():
  try:
    entity = request.args['entity']
  except:
    entity = "*"

  try :
    x = elasticsearch.run_search_uri(es,alert_config,"q=entity.keyword:" + entity + "&size=10000")['hits']
    records = x['hits']
    if entity != "*" :
      try:
        records = records[0]['_source']
      except:
        records = {}
  except :
    records = {}

  return jsonify(records)


################################################################################A
# Metric calls
################################################################################A
# GET
#  /api/v1/metric/last  Get last value for a given metric
#    entity=
#    metric_type=
#    metric_name=
#    metric_value=
#    metric_instance=
@app.route('/api/v1/metric/last', methods=['GET'])
def api_get_metric_last():
  return str(0)
     

# POST
#  /api/v1/metric   Post a new metric
#    entity=
#    metric_name=
#    metric_value=
#    app_id=
@app.route('/api/v1/metric', methods=['POST'])
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



app.run(host='0.0.0.0',port=9000)

