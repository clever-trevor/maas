#!/usr/bin/python3

import json

x = {'entity': 'influxdb', 'metric_class': 'cpu', 'metric_object': 'cpu', 'metric_instance': 'cpu-total', 'metric_name': 'usage_system', 'alert_operator': '<', 'alert_threshold': '1', 'support_team': 'EMS-SUPPORT', 'alert_tag': 'GMS-01', 'last_updated': '23/04/2020 13:47:46'}

print(x)
js = "["
js += json.dumps(x)
js += "]"

print(js)
