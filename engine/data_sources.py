import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_forebet_matches():
    url = "https://www.forebet.com/en/football-predictions"
    matches = []
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for row in soup.select("table.forebet tbody tr"):
            try:
                teams = row.select_one(".homeTeam").get_text(strip=True) + " vs " + row.select_one(".awayTeam").get_text(strip=True)
                league = row.select_one(".league").get_text(strip=True)
                odds = row.select(".odds")
                home_odds = float(odds[0].get_text(strip=True))
                draw_odds = float(odds[1].get_text(strip=True))
                away_odds = float(odds[2].get_text(strip=True))

                matches.append({
                    "MatchID": teams.replace(" ", "_"),
                    "League": league,
                    "HomeOdds": home_odds,
                    "DrawOdds": draw_odds,
                    "AwayOdds": away_odds,
                    "Over1_5Odds": 1.40,
                })
            except Exception as e:
                logging.warning(f"Forebet row parse failed: {e}")
    except Exception as e:
        logging.error(f"Forebet scraper failed: {e}")
    return matches


def get_betmines_matches():
    url = "https://www.betmines.com/football/odds"
    matches = []
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for row in soup.select(".match-row"):
            try:
                teams = row.select_one(".teams").get_text(strip=True)
                league = row.select_one(".league").get_text(strip=True)
                odds = row.select(".odd")
                home_odds = float(odds[0].get_text(strip=True))
                draw_odds = float(odds[1].get_text(strip=True))
                away_odds = float(odds[2].get_text(strip=True))

                matches.append({
                    "MatchID": teams.replace(" ", "_"),
                    "League": league,
                    "HomeOdds": home_odds,
                    "DrawOdds": draw_odds,
                    "AwayOdds": away_odds,
                    "Over1_5Odds": 1.35,
                })
            except Exception as e:
                logging.warning(f"BetMines row parse failed: {e}")
    except Exception as e:
        logging.error(f"BetMines scraper failed: {e}")
    return matches


def get_soccerway_matches():
    url = "https://int.soccerway.com/matches/"
    matches = []
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for row in soup.select(".match"):
            try:
                teams = row.select_one(".team-a").get_text(strip=True) + " vs " + row.select_one(".team-b").get_text(strip=True)
                league = row.select_one(".competition").get_text(strip=True)
                home_odds, draw_odds, away_odds = 1.80, 3.20, 2.10  # placeholder

                matches.append({
                    "MatchID": teams.replace(" ", "_"),
                    "League": league,
                    "HomeOdds": home_odds,
                    "DrawOdds": draw_odds,
                    "AwayOdds": away_odds,
                    "Over1_5Odds": 1.50,
                })
            except Exception as e:
                logging.warning(f"Soccerway row parse failed: {e}")
    except Exception as e:
        logging.error(f"Soccerway scraper failed: {e}")
    return matches


def get_manual_matches():
    """
    Fallback: if scrapers fail, you can paste odds manually here.
    Example: copy from a webpage and fill in dicts.
    """
    return [
        {
            "MatchID": "CHE-ARS",
            "League": "Premier League",
            "HomeOdds": 1.25,
            "DrawOdds": 3.0,
            "AwayOdds": 2.8,
            "Over1_5Odds": 1.30,
        },
        {
            "MatchID": "BAR-SEV",
            "League": "La Liga",
            "HomeOdds": 1.60,
            "DrawOdds": 3.2,
            "AwayOdds": 2.5,
            "Over1_5Odds": 1.40,
        },
    ]


def get_match_data():
    matches = []
    matches.extend(get_forebet_matches())
    matches.extend(get_betmines_matches())
    matches.extend(get_soccerway_matches())

    if not matches:
        logging.warning("No matches scraped. Using manual fallback.")
        matches = get_manual_matches()
    else:
        logging.info(f"Scraped {len(matches)} matches total.")
    return matches
