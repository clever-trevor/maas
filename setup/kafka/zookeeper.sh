cd /app/kafka/kafka
nohup bin/zookeeper-server-start.sh /app/kafka/conf/zookeeper.properties > /app/kafka/logs/zookeeper.log 2>&1 &
