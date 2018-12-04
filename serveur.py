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
                        mailfrom = recv_msg(s)
                        rcptto = recv_msg(s)
                        subject = recv_msg(s)
                        text = recv_msg(s)

                        # verification que c'est un courriel @reseauglo.ca
                        if re.search(r"[@]reseauglo.ca", rcptto):
                            mailto, domain = rcptto.split("@")
                            if os.path.exists(os.getcwd()+"\\"+mailto):
                                print("No function yet")
                            else:
                                os.mkdir(os.getcwd()+"\\"+"DESTERREUR")
                                erreurfile = open(os.getcwd()+"\\"+"DESTERREUR"+"\\DESTERREUR.txt","a")
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
