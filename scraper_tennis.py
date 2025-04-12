from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
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

def scroll_jusqua_fin_matchs(driver):
    max_scrolls = 30
    previous_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def scraper_tennis():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.unibet.fr/sport/tennis?filter=Top+Paris&subFilter=Vainqueur+du+match")
        time.sleep(6)
        scroll_jusqua_fin_matchs(driver)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
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

            except Exception as err:
                continue

        return {"matchs": matchs}

    finally:
        driver.quit()
