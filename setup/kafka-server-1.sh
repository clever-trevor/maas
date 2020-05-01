cd /app/kafka/kafka

ps -ef | grep "kafka-server-1.sh" | grep -v grep | awk '{print $2}' | xargs kill >/dev/null 2>&1

nohup bin/kafka-server-start.sh /app/kafka/conf/server-1.properties &
