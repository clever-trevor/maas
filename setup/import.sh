rm -rf /app/git/maas/maas/api
mkdir -p /app/git/maas/maas/api >/dev/null 2>&1
cp /app/maas/api/* /app/git/maas/maas/api>/dev/null 2>&1

rm -rf /app/git/maas/maas/conf
mkdir -p /app/git/maas/maas/conf >/dev/null 2>&1
cp /app/maas/conf/* /app/git/maas/maas/conf/ >/dev/null 2>&1

rm -rf /app/git/maas/maas/conf/fragments
mkdir -p /app/git/maas/maas/conf/fragments >/dev/null 2>&1
cp /app/maas/conf/fragments/* /app/git/maas/maas/conf/fragments >/dev/null 2>&1

rm -rf /app/git/maas/maas/install
mkdir -p /app/git/maas/maas/install >/dev/null 2>&1
cp /app/maas/install/* /app/git/maas/maas/install >/dev/null 2>&1

rm -rf /app/git/maas/maas/www
mkdir -p /app/git/maas/maas/www/html >/dev/null 2>&1
mkdir -p /app/git/maas/maas/www/scripts >/dev/null 2>&1
mkdir -p /app/git/maas/maas/www/static >/dev/null 2>&1
cp /app/maas/www/* /app/git/maas/maas/www >/dev/null 2>&1
cp /app/maas/www/html/* /app/git/maas/maas/www/html >/dev/null 2>&1
cp /app/maas/www/scripts/* /app/git/maas/maas/www/scripts >/dev/null 2>&1
cp /app/maas/www/static/* /app/git/maas/maas/www/static >/dev/null 2>&1

rm -rf /app/git/maas/telegraf
mkdir -p /app/git/maas/telegraf >/dev/null 2>&1
cp /app/telegraf/telegraf.sh /app/git/maas/telegraf >/dev/null 2>&1

cp /app/maas/installer.sh /app/git/maas >/dev/null 2>&1
  

