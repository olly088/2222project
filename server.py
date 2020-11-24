# TCP message server
from datetime import datetime 
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 1234)) # uses port 1234

s.listen()
connection, address = s.accept()

while True:
    connection.send(bytes("my name jeff".encode('utf-8')))
    print("Server sent")
    time.sleep(10)
