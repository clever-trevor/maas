export ES_PATH_CONF=/app/elk/conf/
cd /app/elk/elasticsearch
nohup /app/elk/elasticsearch/bin/elasticsearch >/dev/null 2>&1 &
