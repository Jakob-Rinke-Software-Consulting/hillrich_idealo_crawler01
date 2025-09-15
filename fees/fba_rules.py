from datetime import datetime

# -------------------------
# Storage Fee Rules (Standardgröße, nicht hazardous)
# -------------------------
STORAGE_FEE = {
    "jan_sep": 27.54,   # €/m³
    "oct_dec": 47.45
}

def calc_storage_fee(volume_m3):
    month = datetime.now().month
    season = "oct_dec" if month in [10, 11, 12] else "jan_sep"
    rate = STORAGE_FEE[season]
    return volume_m3 * rate


# -------------------------
# FBA Size Classes (Europa, stark vereinfacht)
# -------------------------
FBA_SIZE_CLASSES = {
    "small_standard": {"max_weight": 150, "max_dims": (23, 15.5, 0.4), "fee": 1.80},
    "large_standard": {"max_weight": 9000, "max_dims": (45, 34, 26), "fee": 3.50},
    "oversize": {"max_weight": 31000, "max_dims": (120, 60, 60), "fee": 8.00},
}

# Heuristik: Kategorie + Preispunkt → vermutete Größenklasse
CATEGORY_SIZE_MAP = {
    "gl_books": lambda price: "small_standard",
    "gl_clothing": lambda price: "small_standard" if price < 30 else "large_standard",
    "gl_electronics": lambda price: "small_standard" if price < 50 else "large_standard",
    "gl_furniture": lambda price: "oversize",
    "gl_home_kitchen": lambda price: "large_standard" if price > 20 else "small_standard",
    "gl_toys": lambda price: "small_standard" if price < 25 else "large_standard",
    # Fallback
    "default": lambda price: "large_standard",
}


def estimate_size_class(category: str, price: float) -> str:
    func = CATEGORY_SIZE_MAP.get(category, CATEGORY_SIZE_MAP["default"])
    return func(price)


def calc_fulfillment_fee(category: str, price: float) -> float:
    """Nimmt Kategorie+Preis und schätzt die FBA-Größenklasse."""
    size_class = estimate_size_class(category, price)
    return FBA_SIZE_CLASSES[size_class]["fee"]
