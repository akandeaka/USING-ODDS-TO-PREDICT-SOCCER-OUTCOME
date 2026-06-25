def classify_match(match: dict) -> list[dict]:
    """
    Apply blueprint rules to a match and return all triggered signals
    with their associated strength values.
    """

    signals = []

    home = match.get("HomeOdds", 0)
    draw = match.get("DrawOdds", 0)
    away = match.get("AwayOdds", 0)
    over15 = match.get("Over1_5Odds", 0)
    over05ht = match.get("Over0_5HTOdds", 0)
    over25 = match.get("Over2_5Odds", 0)
    under25 = match.get("Under2_5Odds", 0)
    over35 = match.get("Over3_5Odds", 0)
    under15 = match.get("Under1_5Odds", 0)

    # --- Blueprint Rules ---

    # Straight Win Banker
    if 1.22 <= home <= 1.28:
        signals.append({"signal": "Straight Win Banker", "strength": 0.8})

    # BTTS
    if away == 1.75:
        signals.append({"signal": "BTTS", "strength": 0.7})

    # Over 0.5 HT
    if 1.40 <= over05ht <= 1.60:
        signals.append({"signal": "Over 0.5 HT", "strength": 0.7})

    # Over 1.5 Goals
    if 1.20 <= over15 <= 1.40:
        signals.append({"signal": "Over 1.5 Goals", "strength": 0.75})

    # Over 2.5 Goals
    if 1.50 <= over25 <= 1.80:
        signals.append({"signal": "Over 2.5 Goals", "strength": 0.72})

    # Under 2.5 Goals
    if 1.40 <= under25 <= 1.70:
        signals.append({"signal": "Under 2.5 Goals", "strength": 0.68})

    # High-Scoring Banker
    if 2.00 <= over35 <= 2.40:
        signals.append({"signal": "Over 3.5 Goals", "strength": 0.65})

    # Low-Scoring Banker
    if 2.00 <= under15 <= 2.40:
        signals.append({"signal": "Under 1.5 Goals", "strength": 0.65})

    # Draw Banker
    if 2.90 <= draw <= 3.20:
        signals.append({"signal": "Draw Banker", "strength": 0.66})

    # Away Win Banker
    if 2.20 <= away <= 2.60:
        signals.append({"signal": "Away Win Banker", "strength": 0.7})

    return signals
