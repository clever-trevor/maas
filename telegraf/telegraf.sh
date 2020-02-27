ps -ef | grep -v grep | grep telegraf | awk '{print $2}' | xargs kill

host=`hostname | sed -e 's/\..*//g'`
cd /app/telegraf
nohup /app/telegraf/telegraf/usr/bin/telegraf --config "http://192.168.1.113/cgi-bin/telegraf-configure?host=$host&os=linux&reset=true" 2>&1 &
