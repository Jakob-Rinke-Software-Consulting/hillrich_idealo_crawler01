from idealo.idealo_item import IdealoShopItem
from item_filter.amazon_product import AmazonProduct

def check_amazon(item: IdealoShopItem):
    return item.amazon_offer is not None

def check_best(item: IdealoShopItem):
    while item.best_offer is None or item.best_offer.price is None or item.best_offer.price == 0 or item.best_offer.redirectLink == None or not check_shop_blacklist(item):
        try:
            item.best_offer = item.offers.pop()
        except:
            return False
    return True

MIN_AMAZON_RATIO = 1.15
def check_price_ratio(item: IdealoShopItem):
    return item.amazon_offer.price / item.best_offer.price >= MIN_AMAZON_RATIO

MIN_PRICE = 20
def check_min_price(item: IdealoShopItem):
    return item.best_offer.price > MIN_PRICE

MAX_PRICE = 4000
def check_max_price(item: IdealoShopItem):
    return item.best_offer.price < MAX_PRICE

def check_blacklist(item: IdealoShopItem):
    for b in BLACKLIST:
        if b in item.name.lower():
            return False
    return True

def check_word_blacklist(item: IdealoShopItem):
    for b in WORD_BLACKLIST:
        if b in item.name.lower():
            return False
    return True

def check_shop_blacklist(item: IdealoShopItem):
    for b in SHOP_BLACKLIST:
        if b.lower() in item.best_offer.shopName.lower() or b.lower() in item.best_offer.redirectLink.lower():
            return False
    return True

MIN_AMAZON_WIN_RATIO = 0.1
def check_profitablity_90(item: IdealoShopItem):
    marge = get_marge_90(item)
    return marge / item.get_amazon_item().get_avgr90() >= MIN_AMAZON_WIN_RATIO

def check_profitablity_30(item: IdealoShopItem):
    marge = get_marge_30(item)
    return marge / item.get_amazon_item().get_avgr30() >= MIN_AMAZON_WIN_RATIO

def check_profitablity(item: IdealoShopItem):
    marge = get_marge(item)
    return marge / item.amazon_offer.price >= MIN_AMAZON_WIN_RATIO

def get_marge_90(item: IdealoShopItem):
    amz = item.get_amazon_item()
    if amz is None:
        return -1
    avgr90 = amz.get_avgr90()
    print(amz.ean, ", AVGR90:: ", avgr90)
    if avgr90 == -1:
        return -1
    costs = amz.get_cost(item.best_offer.price, avgr90)
    print(amz.ean, "COST90:: ", costs)
    return avgr90 - costs

def get_marge_30(item: IdealoShopItem):
    amz = item.get_amazon_item()
    if amz is None:
        return -1
    avgr30 = amz.get_avgr30()
    print(amz.ean, ", AVGR30:: ", avgr30)
    if avgr30 == -1:
        return -1
    costs = amz.get_cost(item.best_offer.price, avgr30)
    print(amz.ean, "COST30:: ", costs)
    return avgr30 - costs

def get_marge(item: IdealoShopItem):
    amz = item.get_amazon_item()
    if amz is None:
        return -1
    costs = amz.get_cost(item.best_offer.price, item.amazon_offer.price)
    return item.amazon_offer.price - costs


MIN_RATING = 10
MIN_RATING_IF_NO_BSR = 30
MIN_BSR = 50000
def check_selling_amount(item: IdealoShopItem):
    amazon_product = item.get_amazon_item()
    if amazon_product.get_bsr() == -1:
        return amazon_product.get_rating_count() > MIN_RATING_IF_NO_BSR
    return amazon_product.get_bsr() < MIN_BSR

MIN_RATING = 4
def get_min_rating_val(item: IdealoShopItem):
    amazon_product = item.get_amazon_item()
    if amazon_product is None:
        print("No Amazon product found for item:", item.name)
        return False
    return amazon_product.get_rating() >= MIN_RATING

MAX_DOW_DIFF = 1.3
def check_dow_diff(item: IdealoShopItem):
    return item.get_amazon_item().avgr30 / item.amazon_offer.price <= MAX_DOW_DIFF

BUYBOX_BLACKLIST = ["amazon"]
def check_buybox(item: IdealoShopItem):
    buybox = item.get_amazon_item().buybox_seller
    if buybox == "":
        return True
    for b in BUYBOX_BLACKLIST:
        if b.lower() in buybox.lower():
            return False
    return True

MAX_WEIGHT = 3
def check_weight(item: IdealoShopItem):
    return item.get_amazon_item().get_weights_kg() <= MAX_WEIGHT

MIN_SOLD = 50
def filter_sold_last_month(item: IdealoShopItem):
    return item.get_amazon_item().sold_last_month >= MIN_SOLD


with open("settings/marken_blacklist.txt", "r") as f:
    BLACKLIST = f.read().split("\n")
    BLACKLIST = [x.lower().strip() for x in BLACKLIST]

with open("settings/shop_blacklist.txt", "r") as f:
    SHOP_BLACKLIST = f.read().split("\n")
    SHOP_BLACKLIST = [x.lower().strip() for x in SHOP_BLACKLIST]

with open("settings/word_blacklist.txt", "r") as f:
    WORD_BLACKLIST = f.read().split("\n")
    WORD_BLACKLIST = [x.lower().strip() for x in WORD_BLACKLIST]