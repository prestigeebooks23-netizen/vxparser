import os, sys, time

# Ajoute les bons chemins pour que Python trouve tout
rp = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, rp)

try:
    import services
    from utils import common as com
except ImportError as e:
    print(f"Erreur d'importation : {e}")

def main():
    print("=== DEMARRAGE DU SERVEUR ===")
    try:
        # On lance l'initialisation de base
        services.handler('init')
        print("=== SERVEUR IPTV LIVE ===")
    except Exception as e:
        print(f"Erreur au lancement : {e}")
    
    # Garde le serveur allumé
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()


