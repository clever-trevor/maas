HOME=/app/git/maas

mkdir /app/maas/api
cp $HOME/maas/api/* /app/maas/api

mkdir -p /app/maas/conf/fragments
cp $HOME/maas/conf/env.template /app/maas/conf
cp $HOME/maas/conf/fragments/* /app/maas/conf/fragments

mkdir -p /app/maas/install
cp $HOME/maas/install/* /app/maas/install

mkdir -p /app/maas/www/scripts
mkdir -p /app/maas/www/static
mkdir -p /app/maas/www/html
cp $HOME/maas/www/* /app/maas/www
cp $HOME/maas/www/html/* /app/maas/www/html
cp $HOME/maas/www/scripts/* /app/maas/www/scripts
cp $HOME/maas/www/static/* /app/maas/www/static

cd /app/maas/install
/app/maas/install/upload-templates.py

