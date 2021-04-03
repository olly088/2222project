import socket
import time

s = socket.socket()
s.bind(("127.0.0.1", 8000))
s.listen(1)
connection = s.accept()
connection.send(time.ctime() + '\n')
