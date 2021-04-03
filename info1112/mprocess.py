from datetime import datetime
from multiprocessing import Process
import socket

def  send_time(connection):
    connection.send(bytearray("()\n".format(datetime.now().f.encode()


def output_time():
    while True:
        print("Hello World!")
        time.sleep(1)
        proc = Process(target=output_time, args=tuple())
        proc.start()
