import os, sys, time

# Définit le dossier racine pour les imports
rp = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, rp)

def main():
    print("=== TENTATIVE DE DEMARRAGE DU SERVEUR ===")
    try:
        import services
        # On initialise seulement ce qui est nécessaire
        services.handler('init')
        print("=== SERVEUR IPTV VXPARSER OPERATIONNEL ===")
    except Exception as e:
        print(f"Erreur lors du lancement : {e}")
    
    # Garde l'instance active sur Render
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()




