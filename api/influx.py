import urllib.parse
from urllib.request import Request,urlopen
import json

def get_metric(influx_url,query) :
  value = -1
  time_stamp = "NULL"
  try : 
    query = {"q":query}
    data = urllib.parse.urlencode(query).encode('ascii')
    req = Request (influx_url,data)
    resp = json.load(urllib.request.urlopen(req))
    for r in resp['results'] :
      if 'series' in r : 
        for s in r['series'] :
          for v in s['values'] :
            time_stamp = v[0]
            value = v[1]
  except:
    pass
  return value,time_stamp

