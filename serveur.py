#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

"""Script Python qui fonctionne comme un serveur avec relais SMTP qui traite les 
    envois de courriel à l’externe et à l’interne.
    """

__auteur__ = "équipe 22"
__date__ = "2018-12-05"
__coequipiers__ = "François-Joseph Lacroix, Marc-André Boulianne, Marco André Echeverria"

import optparse
import re
import smtplib
import socket
import sys
from socketUtil import recv_msg, send_msg
import os
from email.mime.text import MIMEText
from os.path import getsize

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

                    # Envoi de courriels
                    if (option2 == "1"):
                        mailfrom = recv_msg(s)
                        rcptto = recv_msg(s)
                        subject = recv_msg(s)
                        text = recv_msg(s)

                        # verification que c'est un courriel @reseauglo.ca
                        if re.search(r"[@]reseauglo.ca", rcptto):
                            mailto, domain = rcptto.split("@")
                            if os.path.exists(os.getcwd()+"\\"+mailto):
                                objets1 = []
                                for file in os.listdir(os.getcwd()+"\\"+mailto):
                                    if not file.startswith("config"):
                                        email = open(os.getcwd()+"\\"+mailto+"\\"+file)
                                        lines = email.readlines()
                                        objets1.append(lines[2][10:-1])

                                userfile = open(os.getcwd()+"\\"+mailto+"\\"+str(len(objets1) + 1)+".txt","w")
                                userfile.write("From : " + mailfrom + "\n")
                                userfile.write("To : " + rcptto + "\n")
                                userfile.write("Subject : " + subject + "\n")
                                userfile.write(text)
                                userfile.close()

                            else:
                                if os.path.exists(os.getcwd()+"\\"+"DESTERREUR"):
                                    objetsErreurs = []
                                    for file in os.listdir(os.getcwd()+"\\"+"DESTERREUR"):
                                        if not file.startswith("config"):
                                            email = open(os.getcwd()+"\\"+"DESTERREUR"+"\\"+file)
                                            lines = email.readlines()
                                            objetsErreurs.append(lines[2][10:-1])
                                    erreurfile = open(os.getcwd()+"\\"+"DESTERREUR"+"\\"+str(len(objetsErreurs) + 1)+".txt","w")
                                    erreurfile.write("From : " + mailfrom + "\n")
                                    erreurfile.write("To : " + rcptto + "\n")
                                    erreurfile.write("Subject : " + subject + "\n")
                                    erreurfile.write(text)
                                    erreurfile.close()

                                else:
                                    os.mkdir(os.getcwd()+"\\"+"DESTERREUR")
                                    erreurfile = open(os.getcwd()+"\\"+"DESTERREUR"+"\\1.txt","w")
                                    erreurfile.write("From : " + mailfrom + "\n")
                                    erreurfile.write("To : " + rcptto + "\n")
                                    erreurfile.write("Subject : " + subject + "\n")
                                    erreurfile.write(text)
                                    erreurfile.close()

                        # creation d’un objet courriel avec MIMEText
                        msg = MIMEText(text)
                        msg["From"] = mailfrom
                        msg["To"] = rcptto
                        msg["Subject"] = subject
                    
                        # envoi du courriel grace au protocole SMTP et au serveur de l’universite Laval
                        try:
                            smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
                            smtpConnection.sendmail(mailfrom, rcptto, msg.as_string())
                            smtpConnection.quit()
                            msg2 = "Le courriel a bien ete envoye! "
                            send_msg(s, msg2)
                            
                        except:
                            msg3 = "Le courriel n'a pas ete envoye! "
                            send_msg(s, msg3)

                    # Consultation de courriels
                    if (option2 == "2"):
                        # module qui cherche les messages par sujet
                        objets = []
                        for file in os.listdir(os.getcwd()+"\\"+username):
                            if not file.startswith("config"):
                                email = open(os.getcwd()+"\\"+username+"\\"+file)
                                lines = email.readlines()
                                objets.append(lines[2][10:-1])

                        send_msg(s,str(len(objets)))

                        for objet in objets:
                            send_msg(s,objet)

                        # module qui sélectionne un message de la liste fournie
                        selectemail = eval(recv_msg(s))
                        print (selectemail)

                        for file in os.listdir(os.getcwd()+"\\"+username):
                            if not file.startswith("config"):
                                email = open(os.getcwd()+"\\"+username+"\\"+file)
                                lines = email.readlines()
                                if lines[2][10:-1] == objets[selectemail]:
                                    send_msg(s,lines[0])
                                    send_msg(s,lines[1])
                                    send_msg(s,lines[2])
                                    #concatenate all remaining lines
                                    body = ""
                                    try:
                                        for remainingline in lines[3:]:
                                            body+=remainingline
                                    except:
                                        pass

                                    send_msg(s,body)

                    if (option2 == "3"):
                        # module qui cherche les messages par sujet
                        objets3 = []
                        for file in os.listdir(os.getcwd()+"\\"+username):
                            if not file.startswith("config"):
                                email = open(os.getcwd()+"\\"+username+"\\"+file)
                                lines = email.readlines()
                                objets3.append(lines[2][10:-1])

                        send_msg(s, str(len(objets3)))

                        # module qui calcule la taille du dossier
                        objets4 = []
                        size = 0
                        for file in os.listdir(os.getcwd()+"\\"+username):
                            fileSize = getsize(os.getcwd()+"\\"+username+"\\"+file)
                            size += fileSize

                        globalSize = size
                        send_msg(s, str(globalSize))

                        # module qui envoie les courriels 1 à 1 au client
                        for objet in objets3:
                            send_msg(s,objet)
                        
                    if (option2 == "4"):
                        quitter = True

            else:
                send_msg(s,"Mauvais mot de passe")
                send_msg(s,booleanresult)

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
