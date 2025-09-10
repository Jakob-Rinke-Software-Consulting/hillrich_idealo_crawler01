import requests
import json

with open("settings/keepa_key.txt", "r") as f:
    KEEP_A_KEY = f.read().strip()

API_BASE = "https://api.keepa.com"
API_PRODUCT = API_BASE + "/product"


def get_product_data(asin: str, domain: int = 3):
    t = requests.get(f"{API_PRODUCT}?key={KEEP_A_KEY}&domain={domain}&asin={asin}&history=1&stats=1")
    if t.status_code == 200:
        products = t.json().get("products", [])
        if products:
            return products[0]
        else:
            return -1
    else:
        return -1
    


if __name__ == "__main__":
    with open("test.json", "w") as f:
        json.dump(get_product_data("B07DTGD8KC"), f)
