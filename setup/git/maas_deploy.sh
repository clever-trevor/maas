GITHOME=/app/git/maas/maas
HOME=/app/maas

# Various config scripts
mkdir -p $HOME/conf/fragments
cp -o $GITHOME/conf/env.template $HOME/conf
# Don't overwrite any existing fragments
cp -n $GITHOME/conf/fragments/* $HOME/conf/fragments

# Installer scripts
mkdir -p $HOME/install
cp $GITHOME/install/* $HOME/install

# Initial setup scripts
mkdir -p $HOME/setup
mkdir -p $HOME/setup/elk
mkdir -p $HOME/setup/git
mkdir -p $HOME/setup/influx
mkdir -p $HOME/setup/kafka
mkdir -p $HOME/setup/telegraf
cp $GITHOME/setup/* $HOME/setup
cp $GITHOME/setup/elk/* $HOME/setup/elk
cp $GITHOME/setup/git/* $HOME/setup/git
cp $GITHOME/setup/influx/* $HOME/setup/influx
cp $GITHOME/setup/kafka/* $HOME/setup/kafka
cp $GITHOME/setup/telegraf/* $HOME/setup/telegraf

# Maas Application
mkdir $HOME/api
cp $GITHOME/api/* $HOME/maas/api
mkdir -p $HOME/www
cp $GITHOME/www/* $HOME/www
mkdir -p $HOME/www/html
cp $GITHOME/www/html/* $HOME/www/html
mkdir -p $HOME/www/scripts
cp $GITHOME/www/scripts/* $HOME/www/scripts
mkdir -p $HOME/www/static
cp $GITHOME/www/static/* $HOME/www/static

# Kafka
mkdir -p $HOME/kafka
cp $GITHOME/kafka/* $HOME/kafka

# Now run the script to upload templates
cd $HOME/install
$HOME/install/install.py
$HOME/install/upload-templates.py

