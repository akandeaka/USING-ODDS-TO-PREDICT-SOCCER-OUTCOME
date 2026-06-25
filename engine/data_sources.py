import requests
from bs4 import BeautifulSoup
from datetime import date

def scrape_betmines():
    url = "https://www.betmines.com/football-predictions"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    matches = []
    for card in soup.select(".match-card"):
        try:
            home = float(card.select_one(".odd-home").text)
            draw = float(card.select_one(".odd-draw").text)
            away = float(card.select_one(".odd-away").text)
            matches.append({
                "MatchID": card["data-id"],
                "League": card.select_one(".league-name").text,
                "HomeOdds": home,
                "DrawOdds": draw,
                "AwayOdds": away,
                "Date": str(date.today())
            })
        except Exception:
            continue
    return matches

def scrape_forebet():
    url = "https://www.forebet.com/en/football-predictions"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    matches = []
    for row in soup.select("tr.tr_0, tr.tr_1"):
        try:
            home = float(row.select_one(".odds_home").text)
            draw = float(row.select_one(".odds_draw").text)
            away = float(row.select_one(".odds_away").text)
            matches.append({
                "MatchID": row["data-id"],
                "League": row.select_one(".league").text,
                "HomeOdds": home,
                "DrawOdds": draw,
                "AwayOdds": away,
                "Date": str(date.today())
            })
        except Exception:
            continue
    return matches

def scrape_soccerway():
    url = "https://int.soccerway.com/matches/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    matches = []
    for row in soup.select(".match-row"):
        try:
            home = float(row.select_one(".odd-home").text)
            draw = float(row.select_one(".odd-draw").text)
            away = float(row.select_one(".odd-away").text)
            matches.append({
                "MatchID": row["data-id"],
                "League": row.select_one(".competition").text,
                "HomeOdds": home,
                "DrawOdds": draw,
                "AwayOdds": away,
                "Date": str(date.today())
            })
        except Exception:
            continue
    return matches

def get_match_data():
    matches = []
    for source in [scrape_betmines(), scrape_forebet(), scrape_soccerway()]:
        if source:
            matches.extend(source)
    return matches
