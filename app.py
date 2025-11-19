import os
from tools.crypto import *
from tools.files import *

def main():
    print("Bienvenue sur notre messagerie\n \
    1) Creer un couple de cles\n \
    2) Crypter un message\n \
    3) Decrypter un message\n \
    4) Quitter")
    choice = input("Rentrez une option >>> ")
    if (int(choice) == 1):
        key_creation()
    if (int(choice) == 2):
        message_crypting()
    if (int(choice) == 3):
        message_decrypting()
    
    return 0

def key_creation():
    name = input("Entrez votre nom : ")
    priv, pub = create_keys(name)
    return 0

def message_crypting():
    message = input("Rentrez votre message >>> ")
    dest = input("Qui est le destinataire ? >>> ")

    folder = "my_keys"
    with open(f"{folder}/cle_publique_{dest}.pub", "r") as f:
        lignes = f.read().splitlines()

    n = int(lignes[0])
    e = int(lignes[1])

    print(n, e)

    C = ""
    for i in range(len(message)):
        C += str(codageRSA(ord(message[i]), n, e)) + "\n"
    print(f"{C}")

    f = create_file("message.txt", C)

    return C

def message_decrypting():
    filename = input("Quel est le fichier à décrypter ? >>> ")
    folder = "my_keys"

    with open(f"{folder}/cle_privee", "r") as f:
        lignes = f.read().splitlines()

    n = int(lignes[0])
    d = int(lignes[1])

    with open(f"{filename}", "r") as f:
        lignes = f.read().splitlines()
    M = ""
    for ligne in lignes:
        M += chr(decodageRSA(int(ligne), n, d))

    print(M)

    return 0

    


if __name__ == "__main__":
    main()
