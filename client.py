#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import os
import getpass
from hashlib import sha256

"""Script Python qui implémente l'échange de clé de Diffie-Hellman à l'aide de sockets
    Mode serveur (exemple): python TP3-Q1.py -s -p 3333
    Mode client (exemple): python TP3-Q1.py -d localhost -p 3333
    """

__auteur__ = "équipe 22"
__date__ = "2018-11-07"
__coequipiers__ = "François-Joseph Lacroix, Marc-André Boulianne, Marco André Echeverria"

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

    if (str(option) == "1"): # Se connecter

        # creation du socket et connexion a l’hote distant

        username = input("Nom d'utilisateur : ")
        send_msg(s,username)
        if os.path.exists(os.getcwd()+"\\"+username):
            password = getpass.getpass("Mot de passe : ")
            userfile = open(os.getcwd()+"\\"+username+"\\config.txt","r")
            if userfile.readline() == sha256(password.encode()).hexdigest():
                print ("Vous êtes connecté")
            else:
                print ("Mauvais mot de passe")
            userfile.close()
        else:
            print("L'utilisateur n'existe pas")


    if (str(option) == "2"): # mode client

        destination = (args["address"], args["port"])


        username = input("Nom d'utilisateur : ")
        if os.path.exists(os.getcwd()+"\\"+username):
            print("Cet utilisateur existe déjà")
        else:
            os.mkdir(os.getcwd()+"\\"+username)
            password = getpass.getpass("Mot de passe : ")
            if(any(i.isdigit() for i in password) and any(i.isalpha() for i in password) and len(password)>=6 and len(password)<=12):
                userfile = open(os.getcwd()+"\\"+username+"\\config.txt","w")
                userfile.write(sha256(password.encode()).hexdigest())
                userfile.close()
                print ("Compte créé")
            else:
                print("Le mot de passe doit contenir 6 à 12 caractères dont un chiffre et une lettre")



