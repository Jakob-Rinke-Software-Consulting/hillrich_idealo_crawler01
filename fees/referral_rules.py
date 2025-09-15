# -------------------------
# Referral Fee Rules
# -------------------------
REFERRAL_RULES = {
    "gl_electronics": {"rate": 0.07, "min_fee": 0.30},
    "gl_computers": {"rate": 0.07, "min_fee": 0.30},
    "gl_books": {"rate": 0.15, "min_fee": 1.01},
    "gl_clothing": {
        "price_thresholds": [
            {"up_to": 15.00, "rate": 0.08},
            {"up_to": 45.00, "rate": 0.15},
            {"over": 45.00, "rate": 0.07}
        ],
        "min_fee": 0.30
    },
    "gl_home_kitchen": {"rate": 0.15, "min_fee": 0.30},
    # ... alle deine bisherigen Regeln hier übernehmen ...
    "default": {"rate": 0.11, "min_fee": 0.30}
}


def calc_referral_fee(price, category):
    """Berechnet die Referral Fee abhängig von Kategorie + Preis."""
    rule = REFERRAL_RULES.get(category, REFERRAL_RULES["default"])
    fee = 0.0

    if "price_thresholds" in rule:
        for t in rule["price_thresholds"]:
            if "up_to" in t and price <= t["up_to"]:
                fee = price * t["rate"]
                break
            elif "over" in t and price > t["over"]:
                fee = price * t["rate"]
    else:
        fee = price * rule["rate"]

    return max(fee, rule.get("min_fee", 0))
