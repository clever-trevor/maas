export ES_PATH_CONF=/app/elk/conf/
cd /app/elk/elasticsearch-7.6.0
nohup /app/elk/elasticsearch-7.6.0/bin/elasticsearch >/dev/null 2>&1 &
