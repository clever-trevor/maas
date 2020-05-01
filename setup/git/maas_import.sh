HOME=/app/maas
GITHOME=/app/git/maas

# MaaS API App
rm -rf $GITHOME/api
mkdir -p $GITHOME/api 
cp $HOME/api/* $GITHOME/api

# MaaS Config files
rm -rf $GITHOME/conf
mkdir -p $GITHOME/conf/fragments
cp $HOME/conf/* $GITHOME/conf/ 
cp $HOME/conf/fragments/* $GITHOME/conf/fragments 

# MaaS Installation scripts
rm -rf $GITHOME/install
mkdir -p $GITHOME/install 
cp $HOME/install/* $GITHOME/install 

# MaaS Setup scripts
rm -rf $GITHOME/setup
mkdir -p $GITHOME/setup/elk
mkdir -p $GITHOME/setup/git
mkdir -p $GITHOME/setup/kafka
mkdir -p $GITHOME/setup/influx
mkdir -p $GITHOME/setup/telegraf
cp $HOME/setup/* $GITHOME/setup
cp $HOME/setup/elk/* $GITHOME/setup/elk
cp $HOME/setup/git/* $GITHOME/setup/git
cp $HOME/setup/kafka/* $GITHOME/setup/kafka
cp $HOME/setup/influx/* $GITHOME/setup/influx
cp $HOME/setup/telegraf/* $GITHOME/setup/telegraf

# MaaS Web page app
rm -rf $GITHOME/www
mkdir -p $GITHOME/www/html 
mkdir -p $GITHOME/www/scripts 
mkdir -p $GITHOME/www/static 
cp $HOME/www/* $GITHOME/www 
cp $HOME/www/html/* $GITHOME/www/html 
cp $HOME/www/scripts/* $GITHOME/www/scripts 
cp $HOME/www/static/* $GITHOME/www/static 

# MaaS Kafka consumer
rm -rf $GITHOME/kafka
mkdir -p $GITHOME/kafka
cp $HOME/kafka/* $GITHOME/kafka

