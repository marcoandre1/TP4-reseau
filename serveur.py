import optparse
import re
import smtplib
import socket
import sys
import socketUtil
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

i = 0

isRunning = True
while isRunning:
    # un client se connecte au serveur
    # s est un nouveau socket pour interagir avec le client
    (s, address) = serversocket.accept()

    option = socketUtil.recv_msg(s)
    print (option)

    if(option == "1"):

        print("Connexion")
        #Reception de courriel
        #         # reception du courriel et verification qu’il est valide
        # emailAddress = s.recv(1024).decode()
        #
        #
        # while not re.search(r"^[^@]+@[^@]+\.[^@]+$", emailAddress):
        #     msg = "Saisissez une adresse courriel valide : "
        #     s.send(msg.encode())
        #     emailAddress = s.recv(1024).decode()
        #
        # # creation du courriel
        # courriel = MIMEText("Ce courriel a ete envoye par mon serveur de courriel")
        # courriel["From"] = "exercice3@glo2000.ca"
        # courriel["To"] = emailAddress
        # courriel["Subject"] = "Exercice3"
        #
        # # envoi du courriel
        # try:
        #     smtpConnection = smtplib.SMTP(host="smtp.ulaval.ca", timeout=10)
        #     smtpConnection.sendmail(courriel["From"], courriel["To"], courriel.as_string())
        #     smtpConnection.quit()
        #     msg = "Le courriel a bien ete envoye! "
        #     s.send(msg.encode())
        # except:
        #     msg = "L’envoi n’a pas pu etre effectue. "
        #     s.send(msg.encode())
        #
        # msg = "Au revoir!\n"
        # s.send(msg.encode())


    elif(option == "2"):


        print("création d'utilisateur")


    # s.close()
