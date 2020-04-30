cd /app/maas/api
ps -ef | grep "python3.*api.py" | grep -v grep | awk '{print $2}' | xargs kill
nohup python3 /app/maas/api/api.py > /dev/null 2>&1 &

