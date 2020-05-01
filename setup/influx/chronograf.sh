nohup /app/influx/chronograf/usr/bin/chronograf \
 -b  /app/influx/data/chronograf/chronograf-v1.db \
 > /app/influx/logs/chronograf.log 2>&1 & 
