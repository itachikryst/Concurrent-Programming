import socket
from math import pow

HOST = '127.0.0.1'
PORT = 5000
number = 2

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(str(number).encode())
    data = s.recv(32).decode()
    data = int(data)
print('Received {}'.format(data))
