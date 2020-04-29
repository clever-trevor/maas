
def index():
  import configparser

  maasconf = configparser.RawConfigParser()
  maasconf.read('/app/maas/conf/env')

  f = open("/app/maas/www/html/index","r")
  c = f.read()
  c = c.replace("%KIBANA%",maasconf['kibana']['url'])
  c = c.replace("%CHRONOGRAF%",maasconf['chronograf']['url'])
  c = c.replace("%GRAFANA%",maasconf['grafana']['url'])
  c = c.replace("%PROMETHEUS%",maasconf['prometheus']['url'])

  return c
