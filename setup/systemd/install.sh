cp * /etc/systemd/system
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
