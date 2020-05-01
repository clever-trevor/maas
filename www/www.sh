cd /app/maas/www
ps -ef | grep "python3.*www.py" | grep -v grep | awk '{print $2}' | xargs kill > /dev/null 2>&1
nohup python3 /app/maas/www/www.py > /dev/null 2>&1 &

