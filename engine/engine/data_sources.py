from datetime import date

def get_match_data() -> list[dict]:
    today = str(date.today())
    return [
        {
            "MatchID": "GER001",
            "League": "Bundesliga",
            "HomeOdds": 1.25,
            "DrawOdds": 5.0,
            "AwayOdds": 10.0,
            "Over1_5Odds": 1.30,
            "Over0_5HTOdds": 1.50,
            "Date": today,
        },
        {
            "MatchID": "ENG001",
            "League": "Premier League",
            "HomeOdds": 1.80,
            "DrawOdds": 3.8,
            "AwayOdds": 4.2,
            "Over1_5Odds": 1.35,
            "Over0_5HTOdds": 1.55,
            "Date": today,
        },
    ]

