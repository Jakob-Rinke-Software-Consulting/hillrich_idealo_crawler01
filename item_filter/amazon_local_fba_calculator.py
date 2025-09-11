from datetime import datetime

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
    "gl_health_beauty": {
        "price_thresholds": [
            {"up_to": 10.00, "rate": 0.08},
            {"over": 10.00, "rate": 0.15}
        ],
        "min_fee": 0.30
    },
    "gl_baby_products": {
        "price_thresholds": [
            {"up_to": 10.00, "rate": 0.08},
            {"over": 10.00, "rate": 0.15}
        ],
        "min_fee": 0.30
    },
    "gl_furniture": {
        "price_thresholds": [
            {"up_to": 200.00, "rate": 0.15},
            {"over": 200.00, "rate": 0.10}
        ],
        "min_fee": 0.30
    },
    "gl_tools": {"rate": 0.15, "min_fee": 0.30},
    "gl_grocery": {
        "price_thresholds": [
            {"up_to": 10.00, "rate": 0.08},
            {"over": 10.00, "rate": 0.15}
        ],
        "min_fee": 0.30
    },
    "gl_beverages": {"rate": 0.10, "min_fee": 0.30},
    "gl_automotive": {
        "price_thresholds": [
            {"up_to": 50.00, "rate": 0.15},
            {"over": 50.00, "rate": 0.09}
        ],
        "min_fee": 0.30
    },
    "default": {"rate": 0.15, "min_fee": 0.30}
}

# -------------------------
# Storage Fee Rules (Standardgröße, nicht hazardous)
# -------------------------
STORAGE_FEE = {
    "jan_sep": 27.54,   # €/m³
    "oct_dec": 47.45
}

# -------------------------
# Fulfillment Fee Rules (Standardgröße, Beispielwerte – anpassen falls nötig)
# -------------------------
FBA_FEES = [
    {"max_weight": 150, "fee": 3.22},
    {"max_weight": 400, "fee": 3.50},
    {"max_weight": 900, "fee": 4.20},
    {"max_weight": 14000, "fee": 5.30}
]

# Weight per 10€ of price for rough estimation if no data available
WEIGHT_ESTIMATES_BY_CAT_GL = {
    "gl_electronics": 200,
    "gl_computers": 200,
    "gl_books": 120,
    "gl_clothing": 100,
    "gl_home_kitchen": 180,
    "gl_health_beauty": 70,
    "gl_baby_products": 120,
    "gl_furniture": 350,
    "gl_tools": 250,
    "gl_grocery": 100,
    "gl_beverages": 350,
    "gl_automotive": 250
}

# Volume per 10€ of price for rough estimation if no data available
DIMENSION_ESTIMATES_BY_CAT_GL = {
    "gl_electronics": 0.00018,
    "gl_computers": 0.00018,
    "gl_books": 0.00006,
    "gl_clothing": 0.00009,
    "gl_home_kitchen": 0.00012,
    "gl_health_beauty": 0.00006,
    "gl_baby_products": 0.00009,
    "gl_furniture": 0.0003,
    "gl_tools": 0.00015,
    "gl_grocery": 0.00009,
    "gl_beverages": 0.00018,
    "gl_automotive": 0.00015
}

# -------------------------
# Hilfsfunktionen
# -------------------------
def calc_referral_fee(price, category):
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

def calc_storage_fee(volume_m3):
    month = datetime.now().month
    season = "oct_dec" if month in [10,11,12] else "jan_sep"
    rate = STORAGE_FEE[season]
    return volume_m3 * rate

def calc_fulfillment_fee(weight_g):
    for b in FBA_FEES:
        if weight_g <= b["max_weight"]:
            return b["fee"]
    return FBA_FEES[-1]["fee"]

# -------------------------
# Hauptfunktion
# -------------------------
def get_shipping_fees(item, idealo_price, p):
    # Netto-Umsatz nach Abzug MwSt (19 %)
    category_gl = item.get_cat_gl()
    # Gewicht und Volumen schätzen, falls 0 oder -1
    raw_weight = item.get_weights_kg()
    raw_volume = item.get_dimensions_m3()
    if raw_weight in (0, -1) or raw_weight is None:
        # Use category-based estimate if available, else fallback to 200g per 10€
        weight_per_10 = WEIGHT_ESTIMATES_BY_CAT_GL.get(category_gl, 200)
        weight_g = max(int(p / 10 * weight_per_10), 500)
    else:
        weight_g = max(raw_weight * 1000, 500)

    if raw_volume in (0, -1) or raw_volume is None:
        # Use category-based estimate if available, else fallback to 0.0002 m³ per 10€
        volume_per_10 = DIMENSION_ESTIMATES_BY_CAT_GL.get(category_gl, 0.0002)
        volume_m3 = max((p / 10) * volume_per_10, 0.0001)
    else:
        volume_m3 = max(raw_volume, 0.0001)

    referral = calc_referral_fee(p, category_gl)  # auf Brutto p
    storage = calc_storage_fee(volume_m3)
    fulfillment = calc_fulfillment_fee(weight_g)
    seller_fee = 0.99  # Individual Plan
    cogs = idealo_price  / 0.19  # Wareneinsatz (netto)

    cost_before_tax = referral + storage + fulfillment + seller_fee + cogs
    tax = (p-cost_before_tax) * 0.19
    total_costs = cost_before_tax + tax
    return total_costs