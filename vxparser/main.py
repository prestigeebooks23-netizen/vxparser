import os, sys, time
rp = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, rp)
def main():
    print("=== DEMARRAGE DU SERVEUR ===")
    try:
        import services
        services.handler('init')
        print("=== SERVEUR IPTV LIVE ===")
    except Exception as e:
        print(f"Erreur : {e}")
    while True:
        time.sleep(60)
if __name__ == "__main__":
    main()





