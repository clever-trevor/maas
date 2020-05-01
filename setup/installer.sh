BASE=/app
HOME=$BASE/maas
##############################
# Make Directories

mkdir -p $BASE

mkdir -p $BASE/grafana
mkdir -p $BASE/telegraf
mkdir -p $HOME/api $HOME/conf $HOME/install $HOME/www $HOME/setup
mkdir -p $BASE/git

mkdir -p $BASE/sw

mkdir -p $BASE/influx/data/influxdb
mkdir -p $BASE/influx/data/chronograf
mkdir -p $BASE/influx/data/kapacitor
mkdir -p $BASE/influx/logs
mkdir -p $BASE/influx/conf

mkdir -p $BASE/elk
mkdir -p $BASE/elk/conf
mkdir -p $BASE/elk/data
mkdir -p $BASE/elk/logs

mkdir -p $BASE/kafka
mkdir -p $BASE/kafka/conf
mkdir -p $BASE/kafka/logs

##############################
# Download binaries
cd $BASE/sw

wget https://dl.influxdata.com/influxdb/releases/influxdb-1.8.0_linux_amd64.tar.gz -O influxdb-1.8.0_linux_amd64.tar.gz
wget https://dl.influxdata.com/chronograf/releases/chronograf-1.8.2_linux_amd64.tar.gz -O chronograf-1.8.2_linux_amd64.tar.gz
wget https://dl.influxdata.com/kapacitor/releases/kapacitor-1.5.5_linux_amd64.tar.gz -O kapacitor-1.5.5_linux_amd64.tar.gz
wget https://dl.grafana.com/oss/release/grafana-6.7.3.linux-amd64.tar.gz -O grafana-6.7.3.linux-amd64.tar.gz
wget https://dl.influxdata.com/telegraf/releases/telegraf-1.14.1_linux_amd64.tar.gz -O telegraf-1.14.1_linux_amd64.tar.gz
wget https://github.com/schmorgs/maas/archive/master.zip -O master.zip
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.6.2-linux-x86_64.tar.gz -O elasticsearch-7.6.2-linux-x86_64.tar.gz
wget https://www.apache.org/dyn/closer.cgi?path=/kafka/2.5.0/kafka_2.12-2.5.0.tgz

##############################
# Unzip binaries
##############################

# Influx components
cd $BASE/influx/
tar xzf $BASE/sw/influxdb-1.8.0_linux_amd64.tar.gz
#tar xzf $BASE/sw/chronograf-1.8.2_linux_arm64.tar.gz
tar xzf $BASE/sw/chronograf-1.8.2_linux_amd64.tar.gz
tar xzf $BASE/sw/kapacitor-1.5.5_linux_amd64.tar.gz

# Grafana
cd $BASE/grafana
tar xzf $BASE/sw/grafana-6.7.3.linux-amd64.tar.gz

# Telegraf agent
cd $BASE/telegraf
tar xzf $BASE/sw/telegraf-1.14.1_linux_amd64.tar.gz

# MaaS files
cd $HOME
rm -rf $HOME/api $HOME/install $HOME/setup $HOME/www
mkdir -p $HOME/api $HOME/conf $HOME/install $HOME/www
mkdir -p $HOME/setup/elk  $HOME/setup/git $HOME/setup/influx $HOME/setup/kafka $HOME/setup/telegraf 
unzip -o $BASE/sw/master.zip
cp -r $HOME/maas-master/api/* $HOME/api
# Don't overwrite any existing config files
cp -rn $HOME/maas-master/conf/* $HOME/conf
cp -r $HOME/maas-master/install/* $HOME/install
cp -r $HOME/maas-master/setup/* $HOME/setup > /dev/null 2>&1
cp -r $HOME/maas-master/setup/elk/* $HOME/setup/elk
cp -r $HOME/maas-master/setup/git/* $HOME/setup/git
cp -r $HOME/maas-master/setup/influx/* $HOME/setup/influx
cp -r $HOME/maas-master/setup/kafka/* $HOME/setup/kafka
cp -r $HOME/maas-master/setup/telegraf/* $HOME/setup/telegraf
cp -r $HOME/maas-master/www/* $HOME/www
# Remove rest of repo
rm -rf $HOME/maas-master

# Elasticsearch 
cd $BASE/elk
tar xzf $BASE/sw/elasticsearch-7.6.2-linux-x86_64.tar.gz

# Kafka
cd $BASE/kafka
tar xzf $BASE/sw/kafka_2.12-2.5.0.tgz

##############################
# Symlink binaries to unversions directories
rm -f $BASE/influx/influxdb
ln -s $BASE/influx/influxdb-1.8.0-1 $BASE/influx/influxdb
rm -f $BASE/influx/chronograf
ln -s $BASE/influx/chronograf-1.8.2-1 $BASE/influx/chronograf
rm -f $BASE/influx/kapacitor
ln -s $BASE/influx/kapacitor-1.5.5-1 $BASE/influx/kapacitor
rm -f $BASE/grafana/grafana
ln -s $BASE/grafana/grafana-6.7.3 $BASE/grafana/grafana
rm -f $BASE/elk/elasticsearch
ln -s $BASE/elk/elasticsearch-7.6.2 $BASE/elk/elasticsearch
rm -f $BASE/kafka/kafka
ln -s $BASE/kafka/kafka_2.12-2.5.0 $BASE/kafka/kafka

##############################
# Copy config files only write if they are not already there
cp -n $HOME/setup/influx/influxdb.conf $BASE/influx/conf
cp -n $HOME/setup/influx/kapacitor.conf $BASE/influx/conf
cp -n $HOME/setup/elk/elasticsearch.yml $BASE/elk/conf
cp -n $HOME/setup/elk/kibana.yml $BASE/elk/conf
cp -n $HOME/setup/elk/jvm.options $BASE/elk/conf
cp -n $HOME/setup/elk/log4j2.properties $BASE/elk/conf
cp -n $HOME/setup/kafka/kafka-server-1.properties $BASE/kafka/kafka/conf
cp -n $HOME/setup/kafka/zookeeper.properties $BASE/kafka/kafka/conf

##############################
# Copy startup scripts
cp $HOME/setup/influx/influxdb.sh $BASE/influx
cp $HOME/setup/influx/kapacitor.sh $BASE/influx
cp $HOME/setup/influx/chronograf.sh $BASE/influx
cp $HOME/setup/telegraf/telegraf.sh $BASE/telegraf
cp $HOME/setup/elk/elastic.sh $BASE/elk
cp $HOME/setup/kafka/kafka-server-1.sh $BASE/kafka
cp $HOME/setup/kafka/zookeeper.sh $BASE/kafka

