# works to read the config file and give the date and time of the next time it will run
# just have the thing run, check every sec and then when you execute make it say ran at this time

import time
import sys
import os
import datetime

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

#function returns number corresponding to day of the week in days array
def day_num(day):
    i = 0
    while i < len(days):
        if day.lower() == days[i].lower():
            break
        i += 1
    return i

def count_combos(ls):
    i = 0
    total = 0
    while i < len(ls):
        line_split = status[i].split()
        days_line = line_split[1]
        times_line = line_split[3]
        days_line = days_line.split(",")
        times_line = times_line.split(",")
        total = total + len(times_line)*len(days_line)
        i += 1
    return total

def say_date(day_name):
    day0 = datetime.datetime.now()
    y = day_num(day_name)

    if y == 7:
        sys.exit("Invalid day provided")

    i = 0
    while i < 7:
        if day0.weekday() == y:
            break
        else:
            day0 = day0.replace(day=day0.day + 1)
        i += 1
    
    return day0









#read file into list called status
status = []
f = open("a.conf", "r")
i = 0
while True:
    line = f.readline()
    if line == '':
        f.close()
        break
    status.append(line)
    i += 1

#count combos of time and day
n = count_combos(status)

next_run = []
last_run = []

# cycle through i lines of status, j days and k times
i = 0
while i < len(status):
    line_split = status[i].split()
    days_line = line_split[1]
    times_line = line_split[3]
    days_line = days_line.split(",")
    times_line = times_line.split(",")
    function = ''
    l = 5
    while l < len(line_split):
        function += line_split[l]
        function += " "
        l += 1
    function = function.strip()
    #loop through combos
    j = 0
    while j < len(days_line):
        k = 0
        while k < len(times_line):
            next_date = say_date(days_line[j])
            time_hour = int(times_line[k][0])*10 + int(times_line[k][1])
            time_minute = int(times_line[k][2])*10 + int(times_line[k][3])
            next_date = next_date.replace(hour= time_hour) 
            next_date = next_date.replace(minute = time_minute, second = 0)
            next_run.append("Will run at {} {}".format(next_date.ctime(), function))
            k += 1
        j += 1
    i += 1



#i = 0
#while i < len(next_run):
#    print(next_run[i])
#    i += 1




















#i = 0
#while i < len(days):
    #if x.lower() == days[i].lower():
        #days_to = ((7 + i - weekday) % 7)
        #print("{} days until next {}".format(days_to, days[i]))
        #break
    #i += 1






#print(day)


#days_to = ((day.tue[0] - today.weekday()) % 7)

#print("Days to next {}: {}".format(day.tue[1], days_to))


#delta = datetime.timedelta(7)


#i = 0
#while i < 10:
#    print((today + delta*i).ctime())
#    i += 1


#x = datetime.date(2004, 6, 10).weekday()

#if x == 3:
#    print("Thursday")
