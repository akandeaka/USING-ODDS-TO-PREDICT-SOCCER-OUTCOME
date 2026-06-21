def classify_match(match: dict) -> list[str]:
    signals = []
    home = match["HomeOdds"]
    draw = match["DrawOdds"]
    away = match["AwayOdds"]
    over15 = match["Over1_5Odds"]
    over05ht = match["Over0_5HTOdds"]

    if 1.22 <= home <= 1.28:
        signals.append("Straight Win Banker")
    if away == 1.75:
        signals.append("BTTS")
    if 1.20 <= over15 <= 1.40:
        signals.append("Over 1.5 Goals")
    if 1.40 <= over05ht <= 1.60:
        signals.append("Over 0.5 HT")

    return signals
