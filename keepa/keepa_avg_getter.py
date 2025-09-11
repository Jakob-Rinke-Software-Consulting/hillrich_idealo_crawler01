import requests
import json

try:
    with open("settings/keepa_key.txt", "r") as f:
        KEEP_A_KEY = f.read().strip()
except FileNotFoundError:
    KEEP_A_KEY = ""
    print("No Keepa key found.")

API_BASE = "https://api.keepa.com"
API_PRODUCT = API_BASE + "/product"

FAILED_KEEPA_REQUESTS = 0
def add_save_failed():
    global FAILED_KEEPA_REQUESTS
    FAILED_KEEPA_REQUESTS += 1
    if FAILED_KEEPA_REQUESTS % 20 == 0:
        print("Failed Keepa requests: ", FAILED_KEEPA_REQUESTS)
def get_product_data(asin: str, domain: int = 3):
    if KEEP_A_KEY == "":
        return -1
    t = requests.get(f"{API_PRODUCT}?key={KEEP_A_KEY}&domain={domain}&asin={asin}&history=1&stats=1")
    if t.status_code == 200:
        products = t.json().get("products", [])
        if products:
            return products[0]
        else:
            add_save_failed()
            return -1
    else:
        add_save_failed()
        return -1
    


if __name__ == "__main__":
    with open("test.json", "w") as f:
        json.dump(get_product_data("B07DTGD8KC"), f)
