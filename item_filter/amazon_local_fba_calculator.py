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
    # -------------------------
    # Zusätzliche Kategorien
    # -------------------------
    "gl_sports": {"rate": 0.15, "min_fee": 0.30},
    "gl_outdoors": {"rate": 0.15, "min_fee": 0.30},
    "gl_toys": {"rate": 0.15, "min_fee": 0.30},
    "gl_pet_supplies": {"rate": 0.15, "min_fee": 0.30},
    "gl_jewelry": {
        "price_thresholds": [
            {"up_to": 250.00, "rate": 0.20},
            {"over": 250.00, "rate": 0.05}
        ],
        "min_fee": 0.30
    },
    "gl_watches": {
        "price_thresholds": [
            {"up_to": 250.00, "rate": 0.15},
            {"over": 250.00, "rate": 0.05}
        ],
        "min_fee": 0.30
    },
    "gl_music": {"rate": 0.15, "min_fee": 0.30},
    "gl_video_games": {"rate": 0.15, "min_fee": 0.30},
    "gl_dvd": {"rate": 0.15, "min_fee": 0.30},
    "gl_handmade": {"rate": 0.12, "min_fee": 0.30},
    "gl_office_products": {"rate": 0.15, "min_fee": 0.30},
    "gl_software": {"rate": 0.15, "min_fee": 0.30},
    "gl_instruments": {"rate": 0.15, "min_fee": 0.30},
    "gl_garden": {"rate": 0.15, "min_fee": 0.30},
    "gl_luggage": {"rate": 0.15, "min_fee": 0.30},
    "gl_shoes": {"rate": 0.15, "min_fee": 0.30},
    "gl_personal_care_appliances": {"rate": 0.15, "min_fee": 0.30},
    "gl_large_appliances": {"rate": 0.07, "min_fee": 0.30},
    "gl_small_appliances": {"rate": 0.15, "min_fee": 0.30},
    "gl_industrial": {"rate": 0.12, "min_fee": 0.30},
    "gl_stationery": {"rate": 0.15, "min_fee": 0.30},
    "gl_smartphones": {"rate": 0.07, "min_fee": 0.30},
    "gl_tablets": {"rate": 0.07, "min_fee": 0.30},
    "gl_headphones": {"rate": 0.07, "min_fee": 0.30},
    "gl_video_dvd": {"rate": 0.15, "min_fee": 0.30},
    "gl_pc_components": {"rate": 0.07, "min_fee": 0.30},
    "gl_camera": {"rate": 0.07, "min_fee": 0.30},
    "gl_software_download": {"rate": 0.15, "min_fee": 0.30},
    # Fallback
    "default": {"rate": 0.07, "min_fee": 0.30}
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

# Weight per 10€ of price for rough estimation if no data available (increased values)
WEIGHT_ESTIMATES_BY_CAT_GL = {
    "gl_electronics": 350,
    "gl_computers": 350,
    "gl_books": 200,
    "gl_clothing": 180,
    "gl_home_kitchen": 300,
    "gl_health_beauty": 120,
    "gl_baby_products": 200,
    "gl_furniture": 600,
    "gl_tools": 400,
    "gl_grocery": 180,
    "gl_beverages": 600,
    "gl_automotive": 400,
    "gl_sports": 350,
    "gl_outdoors": 350,
    "gl_toys": 250,
    "gl_pet_supplies": 200,
    "gl_jewelry": 90,
    "gl_watches": 140,
    "gl_music": 180,
    "gl_video_games": 180,
    "gl_dvd": 180,
    "gl_handmade": 180,
    "gl_office_products": 200,
    "gl_software": 180,
    "gl_instruments": 350,
    "gl_garden": 400,
    "gl_luggage": 500,
    "gl_shoes": 250,
    "gl_personal_care_appliances": 200,
    "gl_large_appliances": 1400,
    "gl_small_appliances": 350,
    "gl_industrial": 400,
    "gl_stationery": 180,
    "gl_smartphones": 350,
    "gl_tablets": 350,
    "gl_headphones": 180,
    "gl_video_dvd": 180,
    "gl_pc_components": 350,
    "gl_camera": 350,
    "gl_software_download": 180
}

# Volume per 10€ of price for rough estimation if no data available (increased values)
DIMENSION_ESTIMATES_BY_CAT_GL = {
    "gl_electronics": 0.00035,
    "gl_computers": 0.00035,
    "gl_books": 0.00012,
    "gl_clothing": 0.00018,
    "gl_home_kitchen": 0.00022,
    "gl_health_beauty": 0.00012,
    "gl_baby_products": 0.00018,
    "gl_furniture": 0.0006,
    "gl_tools": 0.00028,
    "gl_grocery": 0.00018,
    "gl_beverages": 0.00035,
    "gl_automotive": 0.00028,
    "gl_sports": 0.00035,
    "gl_outdoors": 0.00035,
    "gl_toys": 0.00022,
    "gl_pet_supplies": 0.00018,
    "gl_jewelry": 0.00006,
    "gl_watches": 0.00008,
    "gl_music": 0.00012,
    "gl_video_games": 0.00012,
    "gl_dvd": 0.00012,
    "gl_handmade": 0.00012,
    "gl_office_products": 0.00018,
    "gl_software": 0.00012,
    "gl_instruments": 0.00035,
    "gl_garden": 0.00028,
    "gl_luggage": 0.00035,
    "gl_shoes": 0.00018,
    "gl_personal_care_appliances": 0.00018,
    "gl_large_appliances": 0.001,
    "gl_small_appliances": 0.00035,
    "gl_industrial": 0.00028,
    "gl_stationery": 0.00012,
    "gl_smartphones": 0.00035,
    "gl_tablets": 0.00035,
    "gl_headphones": 0.00012,
    "gl_video_dvd": 0.00012,
    "gl_pc_components": 0.00035,
    "gl_camera": 0.00035,
    "gl_software_download": 0.00012
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
    cogs = idealo_price  # Einkaufspreis (netto)

    cost_before_tax = referral + storage + fulfillment + seller_fee + cogs
    tax = (p-cost_before_tax) * 0.19
    #print(f"Cost structure:\n Referral: {referral}\n Storage: {storage}\n Fulfillment: {fulfillment}\n Seller Fee: {seller_fee}\n COGS: {cogs}\n")
    total_costs = cost_before_tax + tax
    return total_costs