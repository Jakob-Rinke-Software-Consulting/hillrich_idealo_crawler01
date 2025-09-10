import requests
import time
import random
import concurrent.futures
from threading import Lock

current_proxy_list = []
last_proxy_update = time.time() 

PROXY_UPDATE_FREQUENCY = 3600  # Update every hour

def update_proxy_list():
    global current_proxy_list, last_proxy_update
    try:
        response = requests.get("https://raw.githubusercontent.com/vakhov/fresh-proxy-list/refs/heads/master/socks5.txt")
        if response.status_code == 200:
            current_proxy_list = response.text.splitlines()
            last_proxy_update = time.time()
            print(f"Proxy list updated. Total proxies: {len(current_proxy_list)}")
        else:
            print(f"Failed to update proxy list. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error updating proxy list: {e}")

def remove_invalid_proxies():
    global current_proxy_list
    valid_proxies = []

    def is_proxy_valid(proxy):
        try:
            response = requests.get(
                "https://api.ipify.org",
                proxies={"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"},
                timeout=5
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(is_proxy_valid, current_proxy_list))
        valid_proxies = [proxy for proxy, valid in zip(current_proxy_list, results) if valid]
    current_proxy_list = valid_proxies
    print(f"Invalid proxies removed. Remaining proxies: {len(current_proxy_list)}")
    

update_lock = Lock()
def update_proxies_or_wait_for_update():
    global last_proxy_update
    with update_lock:
        if time.time() - last_proxy_update > PROXY_UPDATE_FREQUENCY or not current_proxy_list:
            update_proxy_list()
            remove_invalid_proxies()
        else:
            print("Waiting for the next proxy update...")

def get_proxy():
    global current_proxy_list, last_proxy_update
    if time.time() - last_proxy_update > PROXY_UPDATE_FREQUENCY or not current_proxy_list:
        update_proxies_or_wait_for_update()
    
    if not current_proxy_list:
        print("No proxies available.")
        raise ValueError("No proxies available. Please update the proxy list.")
    
    proxy = current_proxy_list[random.randint(0, len(current_proxy_list) - 1)]
    return {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}





# test
if __name__ == "__main__":
    update_proxy_list()
    print(f"Current proxy list: {current_proxy_list[:5]}")  # Print first 5 proxies for testing
    print(f"Last update time: {last_proxy_update}")
    print(f"Update frequency: {PROXY_UPDATE_FREQUENCY} seconds")