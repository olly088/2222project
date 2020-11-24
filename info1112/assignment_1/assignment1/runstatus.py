import signal
import time
import os
import sys

# get process-id of runner.py
f = open(".runner.pid", "r")
pid = int(f.readline())
f.close()

# send SIGUSR1 signal to runner.py
os.kill(pid, signal.SIGUSR1)

# open status file in read mode
f = open(".runner.status", "r")
line = f.readline()

# wait 1 second 5 times for runner.py file to write to file then exit after 5 seconds if it hasn't
if line == '':
    i = 0
    while i < 5:
        if line == '':
            time.sleep(1)
            line = f.readline()
            i += 1
        else:
            break
    
        if i == 5:
            print("empty")
            sys.exit("status timeout")

# Print status file to stdout
while True:
    print(line.strip())
    line = f.readline()
    if line == '':
        break

f.close()

# open in write mode and close to truncate to 0 length
f = open(".runner.status", "w")
f.close()
