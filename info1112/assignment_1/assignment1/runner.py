import time as t
import datetime
import sys
import os
import signal

week = datetime.timedelta(days=7)
one_day = datetime.timedelta(days=1)

def get_time(record):
    return record.get("date_and_time")

def get_function_time(day_i, time_stamp_j):

    current_time = datetime.datetime.now() ##convert it to a function after
    weekday = current_time.weekday()
    day_of_function = 0

    k = 0 # finds index of day
    while k < len(day_names):
        if day_i == day_names[k]:
            day_of_function = k 
        k += 1  

    days_to_run = (7 - weekday + day_of_function)%7
    hour_to_run = 10*int(time_stamp_j[0]) + int(time_stamp_j[1])
    minute_to_run = 10*int(time_stamp_j[2]) + int(time_stamp_j[3])

    time = current_time.replace(day=current_time.day+days_to_run, hour=hour_to_run, minute=minute_to_run, second=0, microsecond = 0)

    # deal with at case
    if day_of_function == 7:
        time = time.replace(day=current_time.day)

        if day_of_function != 7:
            time = time + week
        else:
            time = time + one_day

    return time



def receiveSignal(signalNumber, frame):
    caught = True
    status_file = open(".runner.status", "w")

    i = 0
    while i < len(ran):
        if ran[i]["repeat"] == "error":
            line = "error {} {} {}".format(ran[i]["date_and_time"].ctime(), ran[i]["path"], ran[i]["parameters"])
        else:
            line = "ran {} {} {}".format(ran[i]["date_and_time"].ctime(), ran[i]["path"], ran[i]["parameters"])
        status_file.write(line+"\n")
        i += 1

    i = 0
    while i < len(run_queue):
        line = "will run at {} {} {}".format(run_queue[i]["date_and_time"].ctime(), run_queue[i]["path"], run_queue[i]["parameters"])
        status_file.write(line+"\n")
        i += 1

    status_file.close()
    return

# write pid into file
try:
    f = open(".runner.pid", "w")
except IOError as e:
    print("file $HOME/.runner.pid {}".format(e))
    sys.exit()
f.write(str(os.getpid()))
f.close()

# create status file if it doesnt exist
#if not os.pathexistssoenf
try:
    f = open(".runner.status", "w")
except IOError as e:
    print("file $HOME/.runner.status {}".format(e))
    sys.exit()
f.close()
# Parse the config_file and build a list of programs and times to run
try:
    f = open(".runner.conf", "r")
except IOError:
    sys.exit("configuration file not found")



run_queue = []
day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "next possible"]
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
initial = True

while True:    
    line = f.readline()
    if line == '' and initial:
        sys.exit("configuration file empty")
    initial = False

    if line == '':
        break
    
    words = line.split()
    repeat = "once"
    days = None
    time_stamp = None
    path = None
    parameters = ''
    
    if words[0].lower() == "every":
        repeat = "weekly"

    i = 0
    while i < len(words):

        if words[i].lower() == "every" or words[i].lower() == "on":
            days = words[i+1]
            days = days.split(',')

        if words[i].lower() == "at":
            time_stamp = words[i+1]
            time_stamp = time_stamp.split(',')
            if words[0] == "at":
                days = ["next possible"]

        if words[i].lower() == "run":
            try:
                path = words[i+1]
            except IndexError:
                path = None
            parameters = ''
            j = i + 2
            while j < len(words):
                parameters += words[j] + " "
                j += 1

        parameters = parameters.strip()
        i += 1

    # check for every incorrect way
    correct_config = True
    # no run keyword or no path
    if path == None:
        correct_config = False

    i = 0
    while i < len(days):
        # If Dayname is incorrect
        if not days[i] in day_names:
            correct_config = False
        
        # if day has been repeated
        j = i + 1
        while j < len(days):
            if days[i] == days[j]:
                correct_config = False
            j += 1
        i += 1

    i = 0
    while i < len(time_stamp):
        # Time not 4 digits
        if len(time_stamp[i]) != 4:
            correct_config = False
        
        # hour over 24
        if (int(time_stamp[i][0])*10 + int(time_stamp[i][1])) > 23:
            correct_config = False
        
        # part of time not a digit
        j = 0 
        while j < len(time_stamp[i]):
            if not time_stamp[i][j] in digits:
                correct_config = False
            j += 1

        # minute wrong
        if correct_config == True and int(time_stamp[i][2]) > 5:
            correct_config = False

        i += 1
    
    # bad syntax            
    i = 0
    while i < len(words):
        if words[1].lower() == "every" or words[1].lower() == "on" or words[1].lower() == "at":
            correct_config = False
        i += 1

    # path to nowhere
    if not os.path.exists(path):
        correct_config = False

    if correct_config == False:
        sys.exit("error in configuration: {}".format(line))
     
    details = [repeat, days, time_stamp, path, parameters]
    
    # cycle through every combination of day and time and add it to the run_queue
    i = 0
    while i < len(days):
        j = 0
        while j < len(time_stamp):    
            time = get_function_time(days[i], time_stamp[j])

            record = {"repeat":repeat, "date_and_time":time, "path":path, "parameters":parameters}
            run_queue.append(record)
            j += 1
        i += 1

    # check for duplicate times    
    i = 0
    while i < len(run_queue):
        j = i + 1
        while j < len(run_queue):
            if run_queue[i]["date_and_time"] == run_queue[j]["date_and_time"]:
                sys.exit("error in configuration: {}".format(line))
            j += 1
        i += 1


f.close()



run_queue.sort(key=get_time)

 
### put all this shit in a while loop
ran = []
caught = False
first_time = True


while True:    
    signal.signal(signal.SIGUSR1, receiveSignal)

    if caught == True or first_time == True:
        time_to_sleep = run_queue[0]["date_and_time"] - datetime.datetime.now() 
        time_to_sleep = time_to_sleep.total_seconds()
        t.sleep(time_to_sleep)
        first_time == False

    caught = False    

    # fork/exec
    pid = os.fork()
    if pid == 0:
        if run_queue[0]["parameters"] == '':
            os.execl(run_queue[0]["path"], "a")
        else:
            os.execl(run_queue[0]["path"], "a", run_queue[0]["parameters"])
    elif pid == 1:
        errors.append(run_queue[0])
        run_queue[0]["repeat"] = "error"
        
    else:
        ran.append(run_queue[0])
        status = os.wait()

    if run_queue[0]["repeat"].lower() == "every":
        new_record = run_queue[0]
        new_time = new_record["date_and_time"].replace(day=new_record["date_and_time"].day+7)
        new_record["date_and_time"] = new_time
        run_queue.append(new_record)

    run_queue.remove(run_queue[0])

    if len(run_queue) == 0:
        t.sleep(1)
        sys.exit("nothing left to run")

    run_queue.sort(key=get_time)

