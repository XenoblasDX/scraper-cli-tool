# ------ scraping ------

import os
import requests
from bs4 import BeautifulSoup
import time
import msvcrt

from colorama import init, Fore, Style
init(autoreset=True)

# ------ couleurs ------

GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
CYAN = Fore.CYAN
RESET = Style.RESET_ALL
BOLD = Style.BRIGHT

# ------ logo ------

def logo():
    print(GREEN + BOLD + """
   ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
   ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
   ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
   ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
   ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
   ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    """)

    print(CYAN + "═" * 60)
    print(GREEN + "[+] Auteur  : xenoblasdx")
    print(GREEN + "[+] Version : 0.1.2")
    print(GREEN + "[+] Mis à jour : 27/03/2026")
    print(CYAN + "═" * 60)

logo()

# ------ requête HTTP ------

url = "https://www.scrapethissite.com/pages/simple/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def verification_creation_fichier():
    print(f"{GREEN}[✔]{RESET} Lecture du cache...")
    time.sleep(1)
    
    if os.path.exists("scrap1.html"):
        with open("scrap1.html", "r", encoding="utf-8") as f:
            contenu = f.read()
            print(f"{GREEN}[✔]{RESET} Contenu trouvé")
            return contenu
        
    else:
        print(f"{CYAN}[~]{RESET} Connexion en cours...")
        response = requests.get(url, headers=HEADERS)
        response.encoding = "utf-8"
        html = response.text

        if response.status_code == 200:
            print(f"{YELLOW}[...]{RESET} Écriture du fichier...")
            with open("scrap1.html", "w", encoding="utf-8") as f:
                f.write(html)

            print(f"{GREEN}[✔]{RESET} Écriture terminée")
            return html
        else:
            print(f"{RED}[✗]{RESET} Erreur :", response.status_code)
            return None

# ------ parsing ------

code_html = verification_creation_fichier()
soup = BeautifulSoup(code_html, "html.parser")

# ------ extraction ------

def extraction_pays():
    return [p.text.strip() for p in soup.find_all("h3", class_="country-name")]

def extraction_capital():
    return [c.text.strip() for c in soup.find_all("span", class_="country-capital")]

def extraction_population():
    return [p.text.strip() for p in soup.find_all("span", class_="country-population")]

def extraction_area():
    return [a.text.strip() for a in soup.find_all("span", class_="country-area")]

def data_pays():
    data = list(zip(
        extraction_pays(),
        extraction_capital(),
        extraction_population(),
        extraction_area()
    ))
    data.sort()
    return data

# ------ affichage ------

def statistics(l):
    index = 0
    page_size = 20

    while True:
        print("\n" * 2)
        compteur = index + 1

        print(CYAN + "═" * 60)

        for i in l[index:index + page_size]:
            print(f"{YELLOW}{compteur:>3}{RESET} │ {BOLD}{i[0]:<25}{RESET} │ {i[1]:<15} │ {i[2]:<10} │ {i[3]} km²")
            compteur += 1

        print(CYAN + "═" * 60)
        print(GREEN + " A: Menu | Q: précédent | N: suivant ")

        touche = msvcrt.getch().decode("utf-8").lower()

        if touche == "n":
            index += page_size
        elif touche == "q":
            index = max(0, index - page_size)
        elif touche == "a":
            return

# ------ recherche ------

def recherche(l):
    cible = input(f"{YELLOW}[?]{RESET} Pays recherché : ")

    l = sorted(l)
    gauche, droite = 0, len(l) - 1

    while gauche <= droite:
        milieu = (gauche + droite) // 2

        if cible == l[milieu][0]:
            return l[milieu]
        elif l[milieu][0] < cible:
            gauche = milieu + 1
        else:
            droite = milieu - 1

    print(f"{RED}[✗]{RESET} Pays non trouvé")

# ------ menu ------

def menu():
    while True:
        print(CYAN + "═" * 60)
        print(GREEN + "[1] Afficher le code brut")
        print(GREEN + "[2] Rechercher un pays")
        print(GREEN + "[3] Liste des pays")
        print(GREEN + "[4] Actualiser le cache")
        print(GREEN + "[5] Quitter")
        print(CYAN + "═" * 60)
        
        try:
            choix = int(input(GREEN + "Choix > "))

            if choix == 1:
                print(verification_creation_fichier())

            elif choix == 2:
                res = recherche(data_pays())
                if res:
                    print(f"\n{GREEN}[✔]{RESET} Trouvé")
                    print(res)

            elif choix == 3:
                statistics(data_pays())

            elif choix == 4:
                if os.path.exists("scrap1.html"):
                    os.remove("scrap1.html")
                verification_creation_fichier()

            elif choix == 5:
                print("Au revoir")
                return

        except ValueError:
            print(f"{RED}[✗]{RESET} Entrée invalide")

# ------ lancement ------

menu()