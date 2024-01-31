#**Projet RAT Python (Remote Admin tools ) by Mariam CISSE and Mike Arthur NYOGA - 4SI4 ESGI**
	##**Description**
		Ce projet consiste en un ensemble de script Python permettant d'établir une connexion distante entre un client et un serveur, permettant ainsi à l'utilisateur d'exécuter des commandes à distance sur la machine cliente.

	##**Installation**

		###**Prérequis**:
	
		1.Python 3.x installé sur le server et le client.
		2.Les bibliothèques Python requises, telles que socket, subprocess, os, platform, pyautogui, PIL, etc.
	##**Installation des dependances** :
	Pour installer les dépendances Python requises, exécutez la commande suivante dans le dossier "client":
		```pip install -r Client-requirements.txt```
		
	###**Utilisation**

		####**Serveur**:
			1. Exécutez le script server.py sur la machine server en utilisant Python 3.
			2. Attendez que le serveur soit en écoute sur l'adresse IP et le port spécifié.
			3. Une fois qu'une connexion est établie avec un client, vous pouvez utiliser les commandes disponibles pour interagir avec la machine cliente.

		####**Client** :
			1. Exécutez le script client.py sur la machine cliente en utilisant Python 3.
		2. Assurez-vous que le client peut se connecter au server en utilisant l'adresse IP et le port spécifiés.
3. Une fois connecté, vous pouvez recevoir des commandes du server et exécuter des actions sur la machine cliente en fonction de ces commandes.

	
###**Commandes Disponibles**: 

upload: Permet de téléverser un fichier du serveur vers la machine cliente.
download <chemin/du/fichier> <nom_du_fichier>: Permet de télécharger un fichier de la machine cliente vers le serveur.
screenshot: Prend une capture d'écran de la machine cliente et l'envoie au serveur.
shell: Ouvre un shell interactif sur la machine cliente.
ipconfig/ifconfig: Obtient la configuration réseau de la machine cliente.
find/search: Recherche un fichier sur la machine cliente.
hashdump: Récupère le fichier shadow (sur Linux) de la machine cliente et le stocke sur le serveur.
samdump :  Récupère la base SAM (sur Windows) 
