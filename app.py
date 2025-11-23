import tkinter as tk
from tkinter import filedialog
import subprocess
import sys
import os
from tools.crypto import *
from tools.files import *

folder_var = None
distro_var = None

"""
# version CLI
def main():
    choice = 0
    print("Bienvenue sur notre messagerie\n \
    1) Creer un couple de cles\n \
    2) Crypter un message\n \
    3) Decrypter un message\n \
    4) Choisir le dossier des clés\n \
    5) Ouvrir le dossier des clés\n \
    6) Entrer sa distro (si wsl)\n \
    7) Quitter")
    while choice >= 0 and choice < 7:
        choice = int(input("Rentrez une option >>> "))
        if (choice == 1):
            key_creation()
        elif (choice == 2):
            message_crypting()
        elif (choice == 3):
            message_decrypting()
        elif (choice == 4):
            browse_folder()
        elif (choice == 5):
            open_folder()
        elif (choice == 6):
            distro_var.set(input("Distro >>> "))
    
    return 0
"""

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

# ---------- IHM ---------- #

def browse_folder():
    global folder_var

    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_var = folder_selected

def open_folder():
    global folder_var
    global distro_var
    folder = folder_var
    distro = distro_var
    if not folder:
        return

    if sys.platform == "win32":
        os.startfile(folder)
    elif sys.platform == "darwin":
        subporcess.Popen(['open', folder])
    else:
        subprocess.Popen(['explorer.exe', f"\\\\wsl$\\{distro}{folder}"])

def ask_distro():
    popup = tk.Toplevel()
    popup.title("Entrer la distro WSL")
    popup.geometry("300x120")
    popup.grab_set()

    label = tk.Label(popup, text="Nom de la distro wsl :")
    label.pack(pady=10)

    entry = tk.Entry(popup, width=30)
    entry.pack()

    def validate():
        global distro_var
        distro_var = entry.get().strip()

        if distro_var == "" or distro_var == None:
            tk.messagebox.showerror("Erreur", "Veuillez entrer un nom de distribution")
            return

        tk.messagebox.showinfo("OK", f"Distro enregistrée : {distro_var}")
        popup.destroy()

    button = tk.Button(popup, text="Valider", command=validate)
    button.pack(pady=10)

root = tk.Tk()

root.title("Crypteur/Décrypteur")

entry = tk.Entry(root, textvariable=folder_var, width=50)
distro_btn = tk.Button(root, text="Entrer la distro (wsl)", command=ask_distro)
distro_btn.pack(pady=5)
browse_btn = tk.Button(root, text="Parcourir...", command=browse_folder)
browse_btn.pack(pady=5)
open_btn = tk.Button(root, text="Ouvrir le dossier", command=open_folder)
open_btn.pack(pady=5)

root.mainloop()

if __name__ == "__main__":
    main()
