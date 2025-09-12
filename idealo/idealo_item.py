import random
import time
from bs4 import BeautifulSoup
import requests

import proxquest

from item_filter.amazon_product import AmazonProduct

def convert_int(string:str):
    k = int("0" + ''.join(filter(str.isdigit, string.strip().split(" ")[0]))) / 100
    return k 


ITEM_FIND_URL = "https://www.idealo.de/offerpage/offerlist/product/{0}/start/{1}/sort/default"
ITEM_VARIANT_URL = "https://www.idealo.de/offerpage/variantlist/product/{0}/start/{1}0/filters/none"



class IdealoItemHead:

    def __init__(self, name, diplayPrice, link, id):
        self.name = name
        self.displayPrice = convert_int(diplayPrice)
        self.link = link
        self.id = id

    def __str__(self):
        return f"{self.name} - {self.displayPrice}  -> {self.link}"
    
    def get_real_item(self):
        return IdealoShopItem(self.id, self.name)

    def get_all_item_heads(self):
        variants = []
        i = 0
        while True:
            page_src = proxquest.get(ITEM_VARIANT_URL.format(self.id, i), max_of_retries=0, sleep_between_retries=2).text
            soup = BeautifulSoup(page_src, 'html.parser')
            variant_list = soup.find_all("li", class_="productVariants-listItem")
            if not variant_list:
                if len(variants) == 0:
                    return [self]
                else:
                    break
            else:
                for item in variant_list:
                    try:
                        display_price = item.find(class_="priceSup").get_text(strip=True)
                        wrapper = item.find("a", class_="productVariants-listItemWrapper")
                        anker_link = wrapper.get("href")
                        # example link /preisvergleich/OffersOfProduct/201656889_-hf-hp100-3-1000w-heidenfeld.html
                        name = anker_link.split("_")[-1].split(".")[0]
                        id = anker_link.split("/")[-1].split("_")[0]
                        variants.append(IdealoItemHead(name, display_price, anker_link, id))
                    except Exception:
                        continue
                if len(variants) == 0:
                    return [self]
            i += 1
        return variants

class IdealoShopItem:


 
    def __init__(self, id:str, name:str):
        self.amazon_product:AmazonProduct = None
        self.offers = []
        self.id = id
        self.name = name
        self.idealo_listing = "https://www.idealo.de/preisvergleich/OffersOfProduct/" + id + ".html"
        self.offer_url = f"https://www.idealo.de/offerpage/offerlist/product/{id}/start/0/sort/default"
        self.amazon_offer:IdealoItemOffer = None
        self.best_offer:IdealoItemOffer = None
        

        try:
            response = proxquest.get(self.offer_url, max_of_retries=5, timeout=3, sleep_between_retries=2)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Idealo listing page for item {self.name}: {e}")
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        offer_items = soup.select(".productOffers-listItem")
        for item in offer_items:
            of = IdealoItemOffer(self, str(item))
            if (self.best_offer is None) or (self.best_offer.price == 0) or (self.best_offer.price > of.price and of.shopName != "unknown" and of.price > 0):
                self.best_offer = of
            if self.amazon_offer is None and "amazon" in of.shopName:
                self.amazon_offer = of
            self.offers.append(of)
            if self.amazon_offer is not None:
                break

        # sort offers by price
        self.offers.sort(key=lambda x: x.price)

    def __str__(self):
        output =  "Name: " + str(self.name) + "\n"
        output += "Offers: " + str(len(self.offers)) + "\n"
        output += "Best Offer: " + str(self.best_offer) +  "\n"
        output += "Amazon Offer: " + str(self.amazon_offer) + "\n\n"
        return output 
    
    def get_amazon_item(self):
        if self.amazon_product is not None:
            return self.amazon_product
        if self.amazon_offer is None:
            return None
        self.amazon_product = AmazonProduct(self.amazon_offer.redirectLink, self.amazon_offer.price)
        return self.amazon_product


class IdealoItemOffer:

    def __init__(self, item:IdealoShopItem, html):
        self.item = item
        soup = BeautifulSoup(html, 'html.parser')
        try:
            self.nameInShop = soup.find("span", attrs={"class": "productOffers-listItemTitleInner"}).text
        except:
            self.nameInShop = item.name
        try:
            self.price = convert_int(soup.find("a", attrs={"class": "productOffers-listItemOfferPrice"}).text)
        except:
            self.price = 0
        try:
            self.shopName = soup.find("img", attrs={"class": "productOffers-listItemOfferShopV2LogoImage"}).get("alt").split(" ")[0].lower()
        except:
            self.shopName = "unknown"
        try:
            self.redirectLink = "https://idealo.de" + soup.find("a", attrs={"class": "productOffers-listItemOfferLink"}).get("href")
        except:
            self.redirectLink = "unknown"

    def __str__(self) -> str:
        return "Offer for " + str(self.price) + " on " + self.shopName + "   -  " + self.redirectLink
    
    def __hash__(self) -> int:
        return hash(self.shopName)


