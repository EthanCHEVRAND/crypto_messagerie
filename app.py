import tkinter as tk
from tkinter import filedialog
import subprocess
import sys
import os
from tools.crypto import *

folders = {"keys": None, "messages": None}
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

def create_file(filename, content):
    f = open(filename, "x")
    
    with open(filename, "w") as f:
        f.write(content)

    f = open(filename)
    return f

def create_keys():
    global folders
    
    if folders["keys"] == None or folders["keys"] == "":
        tk.messagebox.showerror("Erreur", "Entrer le dossier des clés")
        return
    folder = folders["keys"]

    name = ask_name()

    p, q, e = choixCle(100, 500)
    n_priv, d_priv = clePublique(p, q, e)
    n_pub, e_pub = clePrivee(p, q, e)

    pub = f"{n_pub}\n{e_pub}"
    priv = f"{n_priv}\n{d_priv}"
    
    priv_path = os.path.join(folder, f"cle_privee")
    pub_path  = os.path.join(folder, f"cle_publique_{name}.pub")

    with open(priv_path, "w") as f:
        f.write(priv)

    with open(pub_path, "w") as f:
        f.write(pub)

    priv_key = open(priv_path)
    pub_key = open(pub_path)

    return priv_key, pub_key

# ---------- IHM ---------- #

def browse_folder(fold):
    global folders

    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folders[fold] = folder_selected

def open_folder(fold):
    global folders
    global distro_var
    folder = folders[fold]
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

def ask_name():
    popup = tk.Toplevel()
    popup.title("Entrer votre nom")
    popup.geometry("300x120")
    popup.grab_set()

    label = tk.Label(popup, text="Nom :")
    label.pack(pady=10)

    entry = tk.Entry(popup, width=30)
    entry.pack()

    result = {"name": None}

    def validate():
        name = entry.get().strip()

        if name == "" or name == None:
            tk.messagebox.showerror("Erreur", "Veuillez entrer un nom")
            return

        tk.messagebox.showinfo("OK", f"Nom enregistré : {name}")
        result["name"] = name
        popup.destroy()

    button = tk.Button(popup, text="Valider", command=validate)
    button.pack(pady=10)

    popup.wait_window()
    return result["name"]

root = tk.Tk()

root.title("Crypteur/Décrypteur")

entry = tk.Entry(root, textvariable=folder_var, width=50)

distro_btn = tk.Button(root, text="Entrer la distro (wsl)", command=ask_distro)
distro_btn.pack(pady=5)

browse_btn = tk.Button(root, text="Parcourir dossier clés...", command=lambda: browse_folder("keys"))
browse_btn.pack(pady=5)

open_btn = tk.Button(root, text="Ouvrir le dossier des clés", command=lambda: open_folder("keys"))
open_btn.pack(pady=5)

browse_msg_btn = tk.Button(root, text="Parcourir dossier messages...", command=lambda: browse_folder("messages"))
browse_msg_btn.pack(pady=5)

open_msg_btn = tk.Button(root, text="Ouvrir le dossier des messages", command=lambda: open_folder("messages"))
open_msg_btn.pack(pady=5)

create_keys_btn = tk.Button(root, text="Creer une paire de clés RSA", command=lambda: create_keys())
create_keys_btn.pack(pady=5)

root.mainloop()
