echo "Enter username for the system daemons"
read USER

if [ -z "$USER" ]
then 
  echo "You need supply a username"
  exit
fi

SYSTEMD=/etc/systemd/system
sed "s/%USER%/$USER/g" chronograf.service > $SYSTEMD/chronograf.service
sed "s/%USER%/$USER/g" elasticsearch.service > $SYSTEMD/elasticsearch.service
sed "s/%USER%/$USER/g" grafana.service > $SYSTEMD/grafana.service
sed "s/%USER%/$USER/g" influxdb.service > $SYSTEMD/influxdb.service
sed "s/%USER%/$USER/g" kafka.service > $SYSTEMD/kafka.service
sed "s/%USER%/$USER/g" maas-api.service > $SYSTEMD/maas-api.service
sed "s/%USER%/$USER/g" maas-www.service > $SYSTEMD/maas-www.service
sed "s/%USER%/$USER/g" telegraf.service > $SYSTEMD/telegraf.service
sed "s/%USER%/$USER/g" zookeeper.service > $SYSTEMD/zookeeper.service
exit
systemctl daemon-reload
systemctl enable chronograf 
systemctl enable elasticsearch
systemctl enable grafana
systemctl enable influxdb
systemctl enable kafka
systemctl enable maas-api
systemctl enable maas-www
systemctl enable telegraf
systemctl enable zookeeper
