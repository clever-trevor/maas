ps -ef | grep -v grep | grep chronograf | awk '{print $2}' | xargs kill >/dev/null 2>&1
ps -ef | grep -v grep | grep kapacitor | awk '{print $2}' | xargs kill >/dev/null 2>&1
ps -ef | grep -v grep | grep influxdb | awk '{print $2}' | xargs kill >/dev/null 2>&1

