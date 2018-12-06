#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

"""Script Python qui permet au client d’envoyer et de consulter ses courriels
    """

__auteur__ = "équipe 22"
__date__ = "2018-12-05"
__coequipiers__ = "François-Joseph Lacroix, Marc-André Boulianne, Marco André Echeverria"

import os
import getpass
from hashlib import sha256
import smtplib
from email.mime.text import MIMEText
import re
import argparse
import socket
import sys
from socketUtil import recv_msg, send_msg

# choisissez l’adresse avec l’option -a et le port avec -p
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--address", action="store", dest="address", default="localhost")
parser.add_argument("-p", "--port", action="store", dest="port", type=int, default=1337)
args = vars(parser.parse_args())

# le socket aura besoin d’un tuple contenant l’adresse et le port
destination = (args["address"], args["port"])


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(destination)

isrunning = True
while isrunning:
    print("Menu de connexion")
    print("1. Se connecter")
    print("2. Creer un compte")
    option = input()

    send_msg(s,str(option))

    if (str(option) == "1"): # Se connecter

        username = input("Nom d'utilisateur : ")
        password = getpass.getpass("Mot de passe : ")

        hashedpassword = sha256(password.encode()).hexdigest()

        send_msg(s,username)
        send_msg(s,hashedpassword)

        loginmessage = recv_msg(s)
        print (loginmessage)
        booleanresult = eval(recv_msg(s))

        if booleanresult:
            quitter = False

            while (quitter == False):
                print("Menu principal")
                print("1. Envoi de courriels")
                print("2. Consultation de courriels")
                print("3. Statistiques")
                print("4. Quitter")
                optionMenu = input()
                send_msg(s,str(optionMenu))


                if (str(optionMenu) == "1"):
                    # remplissage des champs par l’utilisateur
                    mailfrom = str(username) + "@reseauglo.ca"
                    send_msg(s, str(mailfrom))

                    rcptto = input("Adresse de destination : ")
                    # verification courriel est valide
                    while not re.search(r"^[^@]+@[^@]+\.[^@]+$", rcptto):
                        print("Saisissez une adresse courriel valide : ")
                    send_msg(s, rcptto)

                    subject = input("Sujet du message : ")
                    send_msg(s, str(subject))

                    print("Data : ")
                    text = ""
                    temp = input()
                    while temp != ".":
                        text += temp + "\n"
                        temp = input()
                    send_msg(s, str(text))

                    response = recv_msg(s)
                    print(response)

                if (str(optionMenu) == "2"):
                    # module qui affiche les messages par sujet
                    print("Consultation de courriels")
                    nbobjets = eval(recv_msg(s))

                    index = 1
                    for i in range(nbobjets):
                        objet = recv_msg(s)
                        print (str(index) + ". " + objet)
                        index +=1

                    print("Sélectionnez un courriel")
                    selectemail = str(eval(input())-1)

                    send_msg(s,selectemail)

                    # mailfrom = recv_msg(s)
                    # mailto = recv_msg(s)
                    # subject = recv_msg(s)
                    # body = recv_msg(s)

                    print(recv_msg(s))
                    print(recv_msg(s))
                    print(recv_msg(s))
                    print(recv_msg(s))

                    print("\nPress enter to exit")
                    exit = input()

                if (str(optionMenu) == "3"):
                    # module qui affiche les messages par sujet
                    print("Consultation de courriels")
                    nbobjets = eval(recv_msg(s))
                    print("Nombre de courriel(s) : "+str(nbobjets))

                    taille = recv_msg(s)
                    print("Taille en octets : " + str(taille))

                    index = 1
                    for i in range(nbobjets):
                        objet = recv_msg(s)
                        print (str(index) + ". " + objet)
                        index +=1

                    #taille = recv_msg(s)
                    #print("Taille en octets : " + str(taille))

                    print("\nPress enter to exit")
                    exit = input()
                    
                if (str(optionMenu) == "4"):
                    quitter = True


    if (str(option) == "2"): # mode client

        username = input("Nom d'utilisateur : ")
        password = getpass.getpass("Mot de passe : ")

        if(any(i.isdigit() for i in password) and any(i.isalpha() for i in password) and len(password)>=6 and len(password)<=12):
            hashedpassword = sha256(password.encode()).hexdigest()

            send_msg(s,username)
            send_msg(s,hashedpassword)

            loginmessage = recv_msg(s)
            print(loginmessage)
        else:
            print("Le mot de passe doit contenir 6 à 12 caractères dont un chiffre et une lettre")




