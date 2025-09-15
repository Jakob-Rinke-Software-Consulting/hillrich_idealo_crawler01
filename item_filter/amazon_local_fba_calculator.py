from fees.referral_rules import calc_referral_fee
from fees.fba_rules import calc_storage_fee, calc_fulfillment_fee

def get_shipping_fees(item, idealo_price, price):
    """
    item: Objekt mit category, optional weight/dimensions (falls verfügbar)
    idealo_price: Einkaufspreis (netto)
    price: Verkaufspreis (brutto)
    """
    category_gl = item.get_cat_gl()

    # Storage: falls keine Maße → Minimalwert annehmen (0.0001 m³)
    raw_volume = item.get_dimensions_m3()
    volume_m3 = raw_volume if raw_volume not in (0, -1, None) else 0.0001
    storage = calc_storage_fee(volume_m3)

    # Fulfillment Fee (auf Basis Kategorie + Preis, nicht Gewichtsschätzung)
    fulfillment = calc_fulfillment_fee(category_gl, price)

    # Referral Fee
    referral = calc_referral_fee(price, category_gl)

    # Seller Fee (Individual Plan)
    seller_fee = 0.99

    # Einkaufskosten (COGS)
    cogs = idealo_price

    # Summieren
    cost_before_tax = referral + storage + fulfillment + seller_fee + cogs

    # USt-Berechnung (19 % auf Marge)
    tax = (price - cost_before_tax) * 0.19
    total_costs = cost_before_tax + tax

    return {
        "referral": referral,
        "storage": storage,
        "fulfillment": fulfillment,
        "seller_fee": seller_fee,
        "cogs": cogs,
        "tax": tax,
        "total_costs": total_costs
    }
