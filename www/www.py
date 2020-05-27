#!/usr/bin/python3

# This is the stub of the MaaS web server. 
# It uses Flask to serve the pages and depending on the URL called,
# will use a Python module to carry out the function
# Everything should be in a "try/except" block to reduce the 
# chance of an untrapped error causing the whole webserver to crash

import flask
from flask import request, jsonify
import urllib.request

# Import the MaaS modules
import sys
sys.path.append("./scripts")
import maas_admin
import maas_alert
import maas_alert_groups
import maas_collect
import maas_conf
import maas_evaluate
import maas_health
import maas_index
import maas_post_metric
import maas_telegraf_configure
import maas_infra

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Home page - do nothing
@app.route('/', methods=['GET'])
def home():
  try:
    content = maas_index.index()
  except:
    content = "<HTML>ERROR</HTML>"
  return content


# Admin functions
@app.route('/admin', methods=['GET'])
def admin():
  args = request.args
  try:
    content = maas_admin.admin(args)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Alert configuration routine
@app.route('/alert', methods=['GET','POST','DELETE'])
def alert():
  args = request.args
  form = request.form
  try:
    content = maas_alert.alert(args,form)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# List ALert Groups
@app.route('/alert-groups', methods=['GET'])
def alert_groups():
  args = request.args
  try:
    content = maas_alert_groups.alert_groups(args)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Configure collection of metrics
@app.route('/collect', methods=['GET','POST'])
def collect():
  args = request.args
  form = request.form
  try:
    content = maas_collect.collect(args,form)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Evaluate alert conditions
@app.route('/evaluate', methods=['GET'])
def evaluate():
  args = request.args
  try:
    content = maas_evaluate.evaluate(args)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Agent health
@app.route('/health', methods=['GET'])
def health():
  args = request.args
  try:
    content = maas_health.health(args)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Check status of Infrastructure components
@app.route('/infra', methods=['GET'])
def infra():
  try:
    content = maas_infra.check()
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Post a sample metric
@app.route('/post-metric', methods=['GET','POST'])
def post_metric():
  form = request.form
  try:
    content = maas_post_metric.post_metric(form)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Called by Telegraf agents to serve configuration
@app.route('/telegraf-configure', methods=['GET'])
def telegraf_configure():
  args = request.args
  try:
    content = maas_telegraf_configure.configure(args)
  except:
    content = "<HTML>ERROR</HTML>"
  return content

# Start the app and listen on all interfaces, port 9000
app.run(host='0.0.0.0',port=9001)

