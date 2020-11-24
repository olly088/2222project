import sys
import os
import time as t
import datetime
import signal


def receiveSignal(signalNumber, frame):
    status_file = open(".runner.status", "w")

    i = 0
    while i < len(queue):
        if queue[i][0] == 1:
            if len (queue[i]) > 4:
                line = "ran {} {} {}".format(queue[i][2].ctime(), queue[i][3], queue[i][4])
            else:
                line = "ran {} {}".format(queue[i][2].ctime(), queue[i][3])
            queue.remove(queue[i])
            i = i - 1
        else:
            if len(queue[i]) > 4:
                line = "will run at {} {} {}".format(queue[i][2].ctime(), queue[i][3], queue[i][4])
            else:
                line = "will run at {} {}".format(queue[i][2].ctime(), queue[i][3])
        line += "\n"
        status_file.write(line)
        i += 1
    status_file.close()
    return


# 1. write pid into file
PID = os.getpid()
PID_file = ".runner.pid"
f = open(PID_file, "w+")
f.write(str(PID))
f.close()

# 2. check for runner.status file/ create it if it doesnt exit
if not os.path.exists(".runner.status"):
    open(".runner.status", 'w+').close()


# read file and deal with it
status = []
f = open(".runner.conf", "r")
i = 0
while True:
    line_info = []
    line = f.readline()
    if line == '':
        break
    split_line = line.split()

    #record keyword as first element in list
    #record days and times and program path and parameters in that order
    if split_line[0].lower() == ("On".lower()):
        line_info.append(0)
        line_info.append(split_line[1])
        line_info.append(split_line[3])
        line_info.append(split_line[5])
        if len(split_line) > 6:
            line_info.append(split_line[6])
    elif split_line[0].lower() == ("Every".lower()):
        line_info.append(1)
        line_info.append(split_line[1]) 
        line_info.append(split_line[3])     
        line_info.append(split_line[5])
        if len(split_line) > 6:
            line_info.append(split_line[6])
    elif split_line[0].lower() == ("At".lower()):
        line_info.append(2)
        line_info.append("tomorrow")
        line_info.append(split_line[1])
        line_info.append(split_line[3])
        if len(split_line) > 4:
            line_info.append(split_line[4])
    else:
        line_info.append(3)

    status.append(line_info)
    i += 1
# Info of config file now stored in status list as multiple lists


#################################################################
#################################################################

# convert to time

# convert days of week to corresponding numbers
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "tomorrow"]

queue = []
current_time = datetime.datetime.now()
weekday = current_time.weekday()

i = 0
while i < len(status):
    # find day specified in function
    days_numbers = []
    status[i][1] = status[i][1].split(',')
    j = 0
    while j < len(status[i][1]):
        k = 0
        while k < 8:
            if str(status[i][1][j]).lower() == days[k].lower():
                #replace day with a number
                days_numbers.append(k)
            k += 1
        j += 1
    status[i][1] = days_numbers

    # convert 4 digits representing time to list containing hour and minute
    times_numbers = []
    status[i][2] = status[i][2].split(',')
    j = 0
    while j < len(status[i][2]):
        hour = int(status[i][2][j][0])*10 + int(status[i][2][j][1]) 
        minute = int(status[i][2][j][2])*10 + int(status[i][2][j][3])
        times_numbers.append([hour, minute])
        j += 1
    status[i][2] = times_numbers
    
    # find day each function should next run
    j = 0
    while j < len(status[i][1]):
        days_to = (7 + status[i][1][j] - weekday)%7
        if status[i][0] == 2:
            do_tomorrow = False
            k = 0
            # at case
            while k < len(status[i][2]):    
                compare_time = current_time.replace(hour=status[i][2][k][0], minute=status[i][2][k][1], second=0, microsecond=0)
                # if all times are in the future than do today otherwise do tomorrow
                if current_time > compare_time:
                    do_tomorrow = True
                k += 1
            days_to = 0 + do_tomorrow

        k = 0
        while k < len(status[i][2]):
            time = current_time.replace(day=current_time.day+days_to, hour=status[i][2][k][0], minute=status[i][2][k][1], second=0, microsecond=0)
            if time < current_time:
                time = time.replace(day=time.day+7)

            queue_entry = [0, status[i][0], time, status[i][3]]
            if len(status[i]) > 4:
                queue_entry.append(status[i][4])
            queue.append(queue_entry)
            k += 1
        j += 1
    i += 1



# sort it by time
new_ls = queue
newer_ls = []

i = 0
while i < len(new_ls):
    earliest = new_ls[0][2]
    index = 0

    j = 0
    while j < len(new_ls):
        if new_ls[j][2] < earliest:
            earliest = new_ls[j][2]
            index = j
        j += 1
        
    newer_ls.append(new_ls[index])
    new_ls.remove(new_ls[index])
        
queue = newer_ls



# add an array that has whats run
# close shit/ process after done with it


while True:
    current_time = datetime.datetime.now()
    i = 0
    while i < len(queue):
        if current_time.ctime() == queue[i][2].ctime():
            forked_pid = os.fork()
            ####
            if forked_pid == 0: # child process executes function
                if len(queue[i]) > 4:
                    os.execl(queue[i][3], "jeff", queue[i][4])
                else:
                    os.execl(queue[i][3], "jeff")
            
            else:  # parent process continues and marks whats been executed
                queue[i][0] = 1 # mark as ran
                if queue[i][1] == 1: # add same process 7 days from now if marked with an every (1)
                    entry_time = queue[i][2]
                    entry_time = queue[i][2].replace(day=entry_time.day+7, second=0, microsecond=0)
                    queue_entry = [0, 1, entry_time, queue[i][3]]
                    if len(queue[i]) > 4:
                        queue_entry.append(queue[i][4])
                    queue.append(queue_entry)

        i += 1

    signal.signal(signal.SIGUSR1, receiveSignal)



    # if recieve a signal cycyle through looking at shit and write it to file in human readable form (ran or to run depending on if first number one or zero.


    t.sleep(1)  # sleep for bit less than a sec







