import os, sys
from time import sleep

# Ajout du chemin pour trouver les modules
rp = os.path.normpath(os.path.dirname(__file__))
sys.path.append(rp)
sys.path.append(os.path.join(rp, 'vxparser'))

import utils.common as com
import services

def main():
    # Force l'initialisation sans menu
    services.handler('init')
    print("Serveur IPTV actif...")
    # Boucle infinie pour garder le serveur allumé
    while True:
        sleep(60)

if __name__ == "__main__":
    main()

