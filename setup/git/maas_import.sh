HOME=/app
GITHOME=/app/git

# MaaS API App
rm -rf $GITHOME/maas/api
mkdir -p $GITHOME/maas/api 
cp $HOME/maas/api/* $GITHOME/maas/api

# MaaS Config files
rm -rf $GITHOME/maas/conf
mkdir -p $GITHOME/maas/conf/fragments
cp $HOME/maas/conf/* $GITHOME/maas/conf/ 
cp $HOME/maas/conf/fragments/* $GITHOME/maas/conf/fragments 

# MaaS Installation scripts
rm -rf $GITHOME/maas/install
mkdir -p $GITHOME/maas/install 
cp $HOME/maas/install/* $GITHOME/maas/install 

# MaaS Setup scripts
rm -rf $GITHOME/maas/setup
mkdir -p $GITHOME/maas/setup/elk
mkdir -p $GITHOME/maas/setup/git
mkdir -p $GITHOME/maas/setup/kafka
mkdir -p $GITHOME/maas/setup/influx
mkdir -p $GITHOME/maas/setup/telegraf
cp $HOME/maas/setup/* $GITHOME/maas/setup
cp $HOME/maas/setup/elk/* $GITHOME/maas/setup/elk
cp $HOME/maas/setup/git/* $GITHOME/maas/setup/git
cp $HOME/maas/setup/kafka/* $GITHOME/maas/setup/kafka
cp $HOME/maas/setup/influx/* $GITHOME/maas/setup/influx
cp $HOME/maas/setup/telegraf/* $GITHOME/maas/setup/telegraf

# MaaS Web page app
rm -rf $GITHOME/maas/www
mkdir -p $GITHOME/maas/www/html 
mkdir -p $GITHOME/maas/www/scripts 
mkdir -p $GITHOME/maas/www/static 
cp $HOME/maas/www/* $GITHOME/maas/www 
cp $HOME/maas/www/html/* $GITHOME/maas/www/html 
cp $HOME/maas/www/scripts/* $GITHOME/maas/www/scripts 
cp $HOME/maas/www/static/* $GITHOME/maas/www/static 

# MaaS Kafka consumer
rm -rf $GITHOME/maas/kafka
mkdir -p $GITHOME/maas/kafka
cp $HOME/maas/kafka/* $GITHOME/maas/kafka

