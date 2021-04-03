PID=`ps -x | grep python | head -n1 | tr -s " " | cut -d " " -f1`
kill -9 $PID
