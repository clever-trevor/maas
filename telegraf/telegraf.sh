source /app/telegraf/telegraf.env
nohup /app/telegraf/telegraf/usr/bin/telegraf --config "http://$CONFIG/telegraf-configure?host=$HOSTSHORT&os=linux&reset=true" >/dev/null 2>&1 &
