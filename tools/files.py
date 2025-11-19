import os
from .crypto import *

def create_file(filename, content):
    f = open(filename, "x")
    
    with open(filename, "w") as f:
        f.write(content)

    f = open(filename)
    return f

def create_keys(name):
    folder = "my_keys"
    os.makedirs(folder, exist_ok=True)

    p, q, e = choixCle(100, 500)
    n_priv, d_priv = clePublique(p, q, e)
    n_pub, e_pub = clePrivee(p, q, e)

    pub = f"{n_pub}\n{e_pub}"
    priv = f"{n_priv}\n{d_priv}"
    
    priv_path = os.path.join(folder, f"cle_privee_{name}")
    pub_path  = os.path.join(folder, f"cle_publique_{name}.pub")

    with open(priv_path, "w") as f:
        f.write(priv)

    with open(pub_path, "w") as f:
        f.write(pub)

    priv_key = open(priv_path)
    pub_key = open(pub_path)

    return priv_key, pub_key

