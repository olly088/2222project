import sys
import os
import signal
import time
# import datetime

# open and read pid file and store value
f = open(".runner.pid", "r")
pid = f.readline()
pid = int(pid)
f.close()

# send SIGUSR1 file with pid
os.kill(pid, signal.SIGUSR1)

time.sleep(1)

# open and read status file and send contents to standard output and then close file
f = open(".runner.status", "r")

text = f.readlines()
i = 0
while i < len(text):
    line = text[i]
    i += 1
    line = line.strip()
    print(line)

f.close()

# re- open it in write mode and then close again to truncate to 0 length

time.sleep(1)

f = open(".runner.status", "w")
f.close()
