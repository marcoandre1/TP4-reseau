import optparse
import re
import smtplib
import socket
import sys
from socketUtil import *
import os
from email.mime.text import MIMEText

# choisissez le port avec l’option -p
parser = optparse.OptionParser()
parser.add_option("-p", "--port", action="store", dest="port", type=int, default=1337)
port = parser.parse_args(sys.argv[1:])[0].port

# creation d’un socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("localhost", port))

# demarre le socket
serversocket.listen(5)
print("Listening on port " + str(serversocket.getsockname()[1]))

(s, address) = serversocket.accept()


isRunning = True
while isRunning:
    # un client se connecte au serveur
    # s est un nouveau socket pour interagir avec le client

    option = recv_msg(s)

    if(option == "1"):
        username = recv_msg(s)
        password = recv_msg(s)

        booleanresult = "False"

        if os.path.exists(os.getcwd()+"\\"+username):
            userfile = open(os.getcwd()+"\\"+username+"\\config.txt","r")
            if userfile.readline() == password:
                send_msg(s,"Vous êtes connecté")
                booleanresult = "True"
                send_msg(s,booleanresult)

                quitter = False

                while (quitter == False):
                    option2 = recv_msg(s)

                    if (option2 == "1"):
                        print("Envoie de courriels")
                    if (option2 == "2"):
                        print("Consultation de courriels")
                    if (option2 == "3"):
                        print("Statistiques")
                    if (option2 == "4"):
                        print("Quitter")
                        quitter = True

            else:
                send_msg(s,"Mauvais mot de passe")

            userfile.close()
        else:
            send_msg(s,"L'utilisateur n'existe pas")
            send_msg(s,booleanresult)



    elif(option == "2"):
        username = recv_msg(s)
        password = recv_msg(s)

        if os.path.exists(os.getcwd()+"\\"+username):
            send_msg(s,"Cet utilisateur existe déjà")
        else:
            os.mkdir(os.getcwd()+"\\"+username)
            userfile = open(os.getcwd()+"\\"+username+"\\config.txt","w")
            userfile.write(password)
            userfile.close()
            send_msg(s,"Votre compte a été créé")


#exit
    # s.close()
