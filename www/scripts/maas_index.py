#!/usr/bin/python3

# This module uses a template for index and replaces variables with the 
# actual endpoints this system is using.

import maas_conf

def index():

  f = open(maas_conf.conf['maas']['base_dir'] + "/www/html/index","r")
  c = f.read()
  c = c.replace("%KIBANA%",maas_conf.conf['kibana']['url'])
  c = c.replace("%CHRONOGRAF%",maas_conf.conf['chronograf']['url'])
  c = c.replace("%GRAFANA%",maas_conf.conf['grafana']['url'])
  c = c.replace("%PROMETHEUS%",maas_conf.conf['prometheus']['url'])

  return c
