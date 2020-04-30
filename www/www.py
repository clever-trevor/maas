#!/usr/bin/python3
#
import flask
from flask import request, jsonify
import urllib.request

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

# Maas configuration variables

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Home page - do nothing
@app.route('/', methods=['GET'])
def home():
  content = maas_index.index()
  return content

@app.route('/admin', methods=['GET'])
def admin():
  args = request.args
  content = maas_admin.admin(args)
  return content

@app.route('/alert', methods=['GET','POST','DELETE'])
def alert():
  args = request.args
  form = request.form
  content = maas_alert.alert(args,form)
  return content

@app.route('/alert-groups', methods=['GET'])
def alert_groups():
  args = request.args
  content = maas_alert_groups.alert_groups(args)
  return content

@app.route('/collect', methods=['GET','POST'])
def collect():
  args = request.args
  form = request.form
  content = maas_collect.collect(args,form)
  return content

@app.route('/evaluate', methods=['GET'])
def evaluate():
  args = request.args
  content = maas_evaluate.evaluate(args)
  return content

@app.route('/health', methods=['GET'])
def health():
  args = request.args
  content = maas_health.health(args)
  return content

@app.route('/post-metric', methods=['GET','POST'])
def post_metric():
  form = request.form
  content = maas_post_metric.post_metric(form)
  return content

@app.route('/telegraf-configure', methods=['GET'])
def telegraf_configure():
  args = request.args
  content = maas_telegraf_configure.configure(args)
  return content

# Start the app and listen on all interfaces, port 9000
app.run(host='0.0.0.0',port=9001)


