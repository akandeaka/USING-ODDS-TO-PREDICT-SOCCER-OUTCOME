# engine/blueprint_classifier.py

def classify_match(match):
    """
    Apply blueprint rules to a match dict.
    Returns a list of signals with confidence scores.
    """
    signals = []

    # Example rules
    if match.get("HomeOdds") and match["HomeOdds"] < 1.50:
        signals.append({"signal": "Straight Win Banker", "strength": 0.85})

    if match.get("Over1_5Odds") and match["Over1_5Odds"] < 1.40:
        signals.append({"signal": "Over 1.5 Goals", "strength": 0.75})

    if match.get("DrawOdds") and match["DrawOdds"] < 3.00:
        signals.append({"signal": "Draw Banker", "strength": 0.65})

    return signals
