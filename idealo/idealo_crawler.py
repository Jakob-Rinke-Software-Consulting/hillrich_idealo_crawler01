from idealo.idealo_item import IdealoItemHead
from idealo.return_thread import ReturnThread
import time
import json
import traceback
from idealo.pool import SyncedIdealoPool
from bs4 import BeautifulSoup
import proxquest


IDEALO_SEARCH_URL = "https://www.idealo.de/preisvergleich/ProductCategory/{0}I16-{1}.html"
IDEALO_SEARCH_URL = "https://www.idealo.de/preisvergleich/MainSearchProductCategory/100I16-{1}.html?q={0}"
JUMPY_BY = 15
MAX_CAT_PAGE = 50
FAILED_REQUESTS = 0

def get_chunk_from_url(self, url):
    global FAILED_REQUESTS, JUMPY_BY
    try:
        if self.page_index > self.max_page:
            self.end()
            return
        try:
            res = proxquest.get(
                url,
                max_of_retries=2, 
                timeout=5,
                sleep_between_retries=1,
                goto_main_first_to_get_session_cookies=True,
                enable_agent=True,
            )
        except Exception as e:
            FAILED_REQUESTS += 1
            if FAILED_REQUESTS  % 20 == 0:
                print("Failed requests: ", FAILED_REQUESTS)
            return
        # if the end url has been redirected to the page without -page_index we assume we reached the end
        if not "-" in res.url and self.page_index > 0:
            raise StopIteration("No more items on page: " + str(self.page_index))
        src = res.text
        soup = BeautifulSoup(src, "html.parser")
        items = soup.select(".sr-resultList__item_m6xdA")
        if len(items) == 0:
            self.end()
            return
        for item in items:
            try:
                title = item.select_one(".sr-productSummary__title_f5flP").get_text(strip=True)
                price = item.select_one(".sr-detailedPriceInfo__price_sYVmx").get_text(strip=True)
                href = item.select("a")[0].get("href")
                id = href.split("/")[-1].split("_")[0]
                head = IdealoItemHead(title, price, href, id)
                try:
                    heads = head.get_all_item_heads()
                except:
                    self.item_keys.add(head.id)
                    self.itemcache.append(head)
                    continue
                for subhead in heads:
                    if subhead.id not in self.item_keys:
                        self.item_keys.add(subhead.id)
                        self.itemcache.append(subhead)
            except Exception as e:
                pass

        self.page_index += 1
    except Exception as e:
        print(f"{self.categoryID} - Error while fetching data: {e} - {url}")
        self.end()


class IdealoCategoryCrawler ():

    def __init__(self, categoryID=-1, max_page=10):
        if categoryID != -1:
            self.categoryID = categoryID
        self.page_index = 0
        self.itemcache = []
        self.item_keys = set()
        self.max_page = max_page


    def __iter__(self):
        self.page_index = 0
        self.itemcache = []
        return self

    def get_next_chunk(self):
        get_chunk_from_url(self, IDEALO_SEARCH_URL.format(self.categoryID, self.page_index*JUMPY_BY))

    def end(self):
        raise StopIteration    
    

    def __next__(self):     
        return self.get_next()
        
    def get_next(self):
        if len(self.itemcache) == 0:
            if self.page_index >= MAX_CAT_PAGE:
                self.end()
                return
            self.get_next_chunk()
            return self.get_next()
        else:
            return self.itemcache.pop()
        
IDEALO_MAIN_CATEGORY_URL = "https://www.idealo.de/preisvergleich/MainSearchProductCategory/100I16-{}oE0oJ4.html"
class MainCategoryCrawler(IdealoCategoryCrawler):
    def __init__(self):
        self.page_index = 0
        self.itemcache = []
        self.item_keys = set()
        self.categoryID = "MainCategory"
        self.max_page = 60

    def get_next_chunk(self):
        get_chunk_from_url(self, IDEALO_MAIN_CATEGORY_URL.format(self.page_index*JUMPY_BY))

    def get_next(self):
        if len(self.itemcache) == 0:
            self.get_next_chunk()
            return self.get_next()
        else:
            return self.itemcache.pop()
    
    def end(self):
        raise StopIteration

    def __next__(self):     
        return self.get_next()


def synced_search(cat, onItem):
    itemsCount = 0  
    crawler = IdealoCategoryCrawler(cat)
    SWITCH = False
    while True:
        try:
            item = crawler.get_next().get_real_item()
            onItem(item)
            itemsCount += 1
            SWITCH = False
        except StopIteration:
            if not SWITCH:
                SWITCH = True
                continue
            break
    return itemsCount

def sync_search_main_category(onItem):
    itemsCount = 0  
    crawler = MainCategoryCrawler()
    while True:
        try:
            item = crawler.get_next().get_real_item()
            onItem(item, "main")
            itemsCount += 1
        except StopIteration:
            if crawler.page_index < 60:
                time.sleep(2)
                continue
            break
    return itemsCount

def loop_search_main_category(onItem):
    while True:
        sync_search_main_category(onItem)

def multi_threaded_synced_search(categories:list, onItem, thread_count=4):
    items = 0
    threads = []
    while len(categories) > 0 or len(threads) > 0:
        # check if any of the threads ended
        for t in threads[:]:
            if not t.is_alive():
                threads.remove(t)
                try:
                    items += t.join()
                except:
                    pass
                del t
        while len(categories) > 0 and len(threads) < thread_count:
            cat = categories.pop()
            t = ReturnThread(target=synced_search, args=(cat, onItem))
            threads.append(t)
            t.start()
        
        time.sleep(10)

    time.sleep(1)
        
    return items
