#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

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

# Menu démarrage client
print("Menu de connexion")
print("1. Se connecter")
print("2. Creer un compte")
text = input()

if (text == "1"): # Se connecter

    # creation du socket et connexion a l’hote distant
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(destination)

    s.close()

if (text == "2"): # mode client

    destination = (args["address"], args["port"])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(destination)

    s.close()

else:
    print("Choisissez l'option 1 ou 2, SVP.")
    s.close()