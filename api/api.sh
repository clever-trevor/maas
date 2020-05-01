cd /app/maas/api
ps -ef | grep "python3.*api.py" | grep -v grep | awk '{print $2}' | xargs kill > /dev/null 2>&1
nohup python3 /app/maas/api/api.py > /dev/null 2>&1 &

