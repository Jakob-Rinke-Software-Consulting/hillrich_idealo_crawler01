import time
import idealo.idealo_crawler as idealo_crawler
from idealo.idealo_item import IdealoShopItem
import item_filter.item_filter as item_filter
from item_filter.amazon_product import AmazonProduct
import requests
import os
import google_writer
import discord_connector
import keepa.keepa_avg_getter as keepa_avg_getter
import threading

def to_csv(item:IdealoShopItem, file="output.csv"):
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write("Name, Buy Price, Current Amazon Price, 30 day Average,BSR, Rating Count,Amazon Link, Idealo Link, Marge, Marge %\n")
    with open(file, "a") as f:
        name = item.name
        buy_price = item.best_offer.price
        cur_amazon_price = item.amazon_offer.price
        avgr30 = item.get_amazon_item().get_avgr90(cur_amazon_price)
        bsr = item.get_amazon_item().get_bsr()
        rating_count = item.get_amazon_item().get_rating_count()
        amazon_link = item.amazon_offer.redirectLink
        idealo_link = item.idealo_listing
        marge = item_filter.get_marge(item)
        marge_percent = marge / item.amazon_offer.price * 100
        f.write(f"{name},{buy_price},{cur_amazon_price},{avgr30},{bsr},{rating_count},\"{amazon_link}\",\"{idealo_link}\",{marge},{marge_percent}\n")


def add_to_writer(item:IdealoShopItem):
    name = item.name
    buy_price = item.best_offer.price
    cur_amazon_price = item.amazon_offer.price
    avgr90 = item.get_amazon_item().get_avgr90()
    avgr30 = item.get_amazon_item().get_avgr30()
    bsr = item.get_amazon_item().get_bsr()
    rating_count = item.get_amazon_item().get_rating_count()
    amazon_link = item.amazon_offer.redirectLink
    idealo_link = item.idealo_listing
    marge = item_filter.get_marge(item)
    marge_percent = marge / item.amazon_offer.price * 100
    marge_90 = item_filter.get_marge_90(item)
    marge_30 = item_filter.get_marge_30(item)
    kategorie = item.get_amazon_item().get_kat_name()
    buybox = item.get_amazon_item().buybox_seller
    anzahl_verkaeufe = item.get_amazon_item().sold_last_month

    data = [name, buy_price, cur_amazon_price, avgr30, avgr90, bsr, rating_count, amazon_link, idealo_link, marge, marge_percent, marge_30, marge_90, kategorie, buybox, anzahl_verkaeufe]
    google_writer.add_to_sheet(data)

        

item_cache = []
item_amount = 0
start_time = time.time()
def onItem(item:IdealoShopItem, channel="all"):
    global item_amount, item_cache
    item_amount += 1
    if item_amount % 100 == 0:
        print(f"Item {item_amount}: Frequency: {item_amount / (time.time() - start_time):.3f} items/second")

    if item_filter.get_filter_val(item) and item.name not in item_cache:
            item_cache.append(item.name)
            print(item)
            #to_csv(item)
            add_to_writer(item)
            
            # Name als Überschrift
            amz_it = item.get_amazon_item()

            # Codeblock starten für Übersicht
            item_str = "```\n"
            item_str += f"{item.name}\n"
            item_str += f"{'Marktplatz':<10} | {'Preis/Wert':>12} | {'30d Avg':>12} | {'90d Avg':>12}\n"
            item_str += f"{'-'*56}\n"

            # Idealo-Zeile (30/90 Tage Durchschnitt nur für Amazon)
            item_str += f"{'Idealo':<10} | {item.best_offer.price:>10.2f} € | {'-':>12} | {'-':>12}\n"

            # Amazon-Zeile
            avg30 = item.get_amazon_item().get_avgr30()
            avg90 = item.get_amazon_item().get_avgr90()
            item_str += f"{'Amazon':<10} | {item.amazon_offer.price:>10.2f} € | {avg30:>10.2f} € | {avg90:>10.2f} €\n"

            item_str += f"{'BSR/Drops':<10} | {amz_it.get_bsr():>12} | {amz_it.get_drop_bsr30():>12} | {amz_it.get_drop_bsr90():>12}\n"

            # Leerzeile nach Tabelle
            item_str += "\n"

            # Weitere Daten darunter, formatiert
            marge_ex, is_exact = item_filter.get_marge_exact(item)
            roi = marge_ex / item.best_offer.price
            marge_percent = marge_ex / item.amazon_offer.price * 100
            marge_label = "Marge (Geschätzt):" if not is_exact else "Marge:"
            roi_label = "ROI (Geschätzt):" if not is_exact else "ROI:"
            item_str += f"{marge_label:<20} {marge_ex:.2f}€ ({marge_percent:.2f}%)\n"
            item_str += f"{roi_label:<20} {roi * 100:.2f}%\n"
            item_str += "```"  # Codeblock schließen

            # Links als Markdown (klickbar, keine Einbettung)
            asin = item.get_amazon_item().ean
            amazon_link = f"https://www.amazon.de/dp/{asin}"
            idealo_link = item.idealo_listing

            item_str += f"[Idealo]({idealo_link}) | [Amazon]({amazon_link})\n"

            # Bild-URL
            img_url = f"https://api.keepa.com/graphimage?key={keepa_avg_getter.KEEP_A_KEY}&asin={asin}&domain=3&range=90&width=800&height=400&type=0&amazon=1&new=1&bb=1&salesrank=1"
            print(img_url)
            # Nachricht senden
            discord_connector.send_message(item_str, img_url, channel)





if __name__ == "__main__":
    ### MAIN PROGRAM ###
    with open("settings/categories.txt", "r") as f:
        category_ids = f.read().split("\n")
        # remove \r and empty strings
        category_ids = [x.strip().replace("\r", "") for x in category_ids]
        category_ids = [x for x in category_ids if x != ""]
    t = time.time()
    # items = idealo_crawler.multi_threaded_category_search(category_ids, onItem)
    import random
    random.shuffle(category_ids)
    t = threading.Thread(target=idealo_crawler.loop_search_main_category, args=(onItem,), daemon=True)
    t.start()
    items = idealo_crawler.multi_threaded_synced_search(category_ids, onItem, 5)
    print("Fetched ", items, " items in ", time.time() - t, " seconds")
    exit(0)
