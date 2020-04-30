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
cp $GITHOME/setup/* $HOME/setup

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

# Now run the script to upload templates
cd $HOME/install
$HOME/install/install.py
$HOME/install/upload-templates.py

