import item_filter.amazon_funcs as amazon_funcs
import item_filter.amazon_local_fba_calculator as amazon_fba_calculator
#import keepa.keepa_price_chart_analyzer as keepa_price_chart_analyzer
import keepa.keepa_avg_getter as keepa_avg_getter
from selenium.webdriver.common.by import By
import time
import proxquest
from bs4 import BeautifulSoup
import keepa.keepa_avg_getter as keepa_avg_getter


class AmazonProduct:

    def __init__(self, url, price=0):
        self.price = price 
        self.soup = -1
        self.fba_costs = -1
        self.avgr30 = -1
    
        try:
            req = proxquest.get(url, enable_proxy=False, timeout=3, max_of_retries=0)
            self.page_src = req.text
            soup = BeautifulSoup(self.page_src, 'html.parser')
            self.ean = amazon_funcs.get_ean(req.url)
        except Exception as e:
            print("Error fetching Amazon product page:", e)
            self.page_src = ""
            soup = BeautifulSoup("", 'html.parser')
            self.ean = ""
        # Extract buybox_seller using BeautifulSoup
        try:
            expander = soup.find(id="merchantInfoFeature_feature_div")
            if expander:
                d = expander.find(class_="offer-display-feature-text")
                if d:
                    span = d.find("span")
                    self.buybox_seller = span.get_text(strip=True) if span else ""
                    if self.buybox_seller == "":
                        self.buybox_seller = "???"
                else:
                    self.buybox_seller = ""
            else:
                self.buybox_seller = ""
        except Exception:
            self.buybox_seller = ""

        # Extract sold_last_month using BeautifulSoup
        try:
            l = soup.find(id="social-proofing-faceout-title-tk_bought")
            if l:
                span = l.find("span")
                if span:
                    sold_text = span.get_text(strip=True)
                    sold_digits = ''.join(filter(str.isdigit, sold_text))
                    self.sold_last_month = int(sold_digits) if sold_digits else -1
                else:
                    self.sold_last_month = -1
            else:
                self.sold_last_month = -1
        except Exception:
            self.sold_last_month = -1
            self.sold_last_month = -1

        self.weight = -1
        self.kat_name = -1
        self.cost_cache = {}
        self.keepa_data = -1



    def get_bsr(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        if self.keepa_data != -1:
            rank_table = self.keepa_data["salesRanks"]
            if rank_table:
                return max([
                    cat[-1] for cat in rank_table.values() 
                ])
        else:
            print("Warning: No Keepa data available for BSR retrieval.")
        return amazon_funcs.get_bsr(self.soup)
    
    def get_rating_count(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_rating_count(self.soup)
    
    def get_amazon_soup(self):
        return amazon_funcs.get_amazon_json(self.ean)
    
    def get_dimensions_m3(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_dimensions_m3(self.soup)
    

    def get_cost(self, idealo_price, p, force=False):
        for key in self.cost_cache:
            if key[0] == idealo_price and key[1] == p and not force:
                return self.cost_cache[key]
        self.fba_costs = amazon_fba_calculator.get_shipping_fees(self, idealo_price, p)
        print(f"FBA Costs for item {self.ean} at price {p}/{idealo_price/1.19}: {self.fba_costs}")
        self.cost_cache[(idealo_price, p)] = self.fba_costs
        return self.fba_costs
    
    def get_cat_gl(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_cat(self.soup)
    
    def get_rating(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_rating(self.soup)
    
    def get_avgr90(self):
        if self.keepa_data == -1:
            self.keepa_data = keepa_avg_getter.get_product_data(self.ean)
        if self.keepa_data == -1:
            return -1
        stats = self.keepa_data.get("stats", {})
        if not stats:
            return -1
        avgr90 = stats.get("avg90", -1)
        if avgr90 == -1:
            return -1
        avgr90 = avgr90[1]
        return avgr90 / 100

    def get_avgr30(self):
        if self.keepa_data == -1:
            self.keepa_data = keepa_avg_getter.get_product_data(self.ean)
        if self.keepa_data == -1:
            return -1
        stats = self.keepa_data.get("stats", {})
        if not stats:
            return -1
        avgr30 = stats.get("avg30", -1)
        if avgr30 == -1:
            return -1
        avgr30 = avgr30[1]
        return avgr30 / 100

    
    def get_weights_kg(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_weights_kg(self.soup)

    def get_kat_name(self):
        if self.soup == -1:
            self.soup = amazon_funcs.get_amazon_json(self.ean)
        return amazon_funcs.get_kat_name(self.soup)
    
    def get_drop_bsr30(self):
        if self.keepa_data == -1:
            self.keepa_data = keepa_avg_getter.get_product_data(self.ean)
        if self.keepa_data == -1:
            return -1
        stats = self.keepa_data.get("stats", {})
        if not stats:
            return -1
        return stats.get("salesRankDrops30", -1)
    
    def get_drop_bsr90(self):
        if self.keepa_data == -1:
            self.keepa_data = keepa_avg_getter.get_product_data(self.ean)
        if self.keepa_data == -1:
            return -1
        stats = self.keepa_data.get("stats", {})
        if not stats:
            return -1
        return stats.get("salesRankDrops90", -1)

    

    def __str__(self):
        return f"AmazonProduct(ean={self.ean}, price={self.price}, buybox_seller={self.buybox_seller}, sold_last_month={self.sold_last_month})"

