from idealo.idealo_item import IdealoShopItem
from item_filter.filter_funcs import *

default_filter_funcs = [
    check_amazon, 
    check_best,
    check_price_ratio, 
    check_min_price,
    check_max_price,
    check_blacklist,
    check_word_blacklist,
    #get_min_rating_val,
    #check_weight,
    #check_buybox,
    check_profitablity,
    check_profitablity_30,
    check_selling_amount,
    check_profitablity_90
]


def get_filter_func_by_name(name:str):
    for f in default_filter_funcs:
        if f.__name__ == name:
            return f
    return None


FILTER_FUNCS = []
with open("settings/filters.txt", "r") as f:
    # style: func=1 or 0   (1 = include, 0 = exclude)
    for line in f:
        line = line.strip()
        if line == "" or line.startswith("#"):
            continue
        parts = line.split("=")
        if len(parts) != 2:
            print(f"Invalid filter line: {line}")
            continue
        func_name = parts[0].strip()
        include = parts[1].strip() == "1"
        func = get_filter_func_by_name(func_name)
        if func is None:
            print(f"Filter function not found: {func_name}")
            continue
        if include:
            FILTER_FUNCS.append(func)

def get_filter_val(item: IdealoShopItem, filter_funcs:list=FILTER_FUNCS):
    for f in filter_funcs:
        if not f(item):
            return False
    return True


    