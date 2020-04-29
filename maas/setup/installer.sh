##############################
# Make Directories

mkdir -p /app

mkdir -p /app/grafana
mkdir -p /app/telegraf
mkdir -p /app/maas
mkdir -p /app/git

mkdir -p /app/sw

mkdir -p /app/influx/data/influxdb
mkdir -p /app/influx/data/chronograf
mkdir -p /app/influx/data/kapacitor
mkdir -p /app/influx/logs
mkdir -p /app/influx/conf

mkdir -p /app/elk
mkdir -p /app/elk/conf
mkdir -p /app/elk/data
mkdir -p /app/elk/logs

##############################
# Download binaries
cd /app/sw

wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.0_linux_amd64.tar.gz -O influxdb-1.8.0_linux_amd64.tar.gz
#wget https://dl.influxdata.com/chronograf/releases/chronograf-1.8.2_linux_arm64.tar.gz -O chronograf-1.8.2_linux_arm64.tar.gz
wget https://dl.influxdata.com/chronograf/releases/chronograf-nightly_linux_amd64.tar.gz -O chronograf-nightly_linux_amd64.tar.gz
wget https://dl.influxdata.com/kapacitor/releases/kapacitor-1.5.5_linux_amd64.tar.gz -O kapacitor-1.5.5_linux_amd64.tar.gz
wget https://dl.grafana.com/oss/release/grafana-6.7.3.linux-amd64.tar.gz -O grafana-6.7.3.linux-amd64.tar.gz
wget https://dl.influxdata.com/telegraf/releases/telegraf-1.14.1_linux_amd64.tar.gz -O telegraf-1.14.1_linux_amd64.tar.gz
wget https://github.com/schmorgs/maas/archive/master.zip -O master.zip
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz -O elasticsearch-7.6.2-linux-x86_64.tar.gz

##############################
# Unzip binaries
cd /app/influx/
tar xzf /app/sw/influxdb-1.8.0_linux_amd64.tar.gz
tar xzf /app/sw/chronograf-1.8.2_linux_arm64.tar.gz
tar xzf /app/sw/chronograf-nightly_linux_amd64.tar.gz
tar xzf /app/sw/kapacitor-1.5.5_linux_amd64.tar.gz
cd /app/grafana
tar xzf /app/sw/grafana-6.7.3.linux-amd64.tar.gz

cd /app/telegraf
tar xzf /app/sw/telegraf-1.14.1_linux_amd64.tar.gz

cd /app/maas
rm -rf api install www
unzip -o /app/sw/master.zip
mkdir -p /app/maas/api /app/maas/api/conf /app/maas/install /app/maas/www
cp -r /app/maas/maas-master/maas/api/* /app/maas/api
cp -rn /app/maas/maas-master/maas/conf/* /app/maas/api/conf
cp -r /app/maas/maas-master/maas/install/* /app/maas/install
cp -r /app/maas/maas-master/maas/www/* /app/maas/www
rm -rf /app/maas/maas-master
rm -rf /app/maas/maas

cd /app/elk
tar xzf /app/sw/elasticsearch-7.6.2-linux-x86_64.tar.gz

##############################
# Create unversioned symlinks
rm -f /app/influx/influxdb
ln -s /app/influx/influxdb-1.8.0-1 /app/influx/influxdb
rm -f /app/influx/chronograf
ln -s /app/influx/chronograf-202004242133~nightly-0 /app/influx/chronograf
rm -f /app/influx/kapacitor
ln -s /app/influx/kapacitor-1.5.5-1 /app/influx/kapacitor
rm -f /app/grafana/grafana
ln -s /app/grafana/grafana-6.7.3 /app/grafana/grafana
rm -f /app/elk/elastic
ln -s /app/elk/elasticsearch-7.6.2 /app/elk/elastic

##############################
# Copy config files only write if they are not already there
cp -n /app/sw/influx/conf/* /app/influx/conf

cp -n /app/sw/elastic/*yml /app/elk/conf
cp -n /app/sw/elastic/*options /app/elk/conf
cp -n /app/sw/elastic/*properties /app/elk/conf

##############################
# Copy startup scripts
cp /app/sw/influx/conf/*.sh /app/influx
cp /app/sw/telegraf/*.sh /app/telegraf
cp /app/sw/elastic/*.sh /app/elk

