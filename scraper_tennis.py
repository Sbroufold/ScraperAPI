import requests
from bs4 import BeautifulSoup
import unicodedata
import re

def normaliser(nom):
    termes_a_ignorer = [
        "usa", "fra", "esp", "ger", "chi", "rus", "col", "aus", "mar",
        "arg", "pol", "ita", "ned", "jpn", "swe", "can", "ukr", "kor", "cze", "srb", "tpe"
    ]
    nom = unicodedata.normalize('NFKD', nom).encode('ASCII', 'ignore').decode()
    for terme in termes_a_ignorer:
        nom = nom.replace(terme, '')
    nom = re.sub(r'[^a-zA-Z]', '', nom).lower()
    return nom

def scraper_tennis():
    url = "https://www.unibet.fr/sport/tennis?filter=Top+Paris&subFilter=Vainqueur+du+match"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.select("section.eventcard--toplight")

        matchs = []
        for e in events:
            try:
                equipes = e.select("h2")
                if len(equipes) != 2:
                    continue
                team1 = equipes[0].text.strip()
                team2 = equipes[1].text.strip()
                nom_match = f"{team1} - {team2}"

                valeurs = e.select(".oddbox-value span")
                cotes = []
                for v in valeurs[:2]:
                    try:
                        cote = float(v.text.strip().replace(',', '.'))
                        cotes.append(cote)
                    except:
                        continue

                heure_div = e.select_one(".eventcard-header-meta")
                heure = heure_div.text.strip().split()[0] if heure_div else "?"

                if len(cotes) == 2:
                    matchs.append({
                        "match": nom_match,
                        "cotes": cotes,
                        "heure": heure
                    })
            except:
                continue

        return {"matchs": matchs}

    except Exception as e:
        return {"error": str(e)}

