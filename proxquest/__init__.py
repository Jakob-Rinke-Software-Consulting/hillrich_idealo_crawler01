try:
    import proxquest.proxy_manager as proxy_manager
    import proxquest.agents as agents
except ImportError:
    import proxy_manager
    import agents
import requests
import time
import random

SESSION_NUM = 300
SESSIONS = []
SESSION_RESET_CHANCE = 1 / 100
for i in range(SESSION_NUM):
    SESSIONS.append(requests.Session())
def get_random_session():
    index = random.randint(0, SESSION_NUM - 1)
    if random.random() < SESSION_RESET_CHANCE:
        SESSIONS[index] = requests.Session()
    return SESSIONS[index]
    

def get(url, max_of_retries=3, timeout=2, sleep_between_retries=0.3, retry_on_status=False, enable_agent=True, enable_proxy=False, goto_main_first_to_get_session_cookies=False, *args, **kwargs):
    """
    Makes a GET request to the specified URL using a random user agent and a proxy.
    """
    retries = 0
    while True:
        session: requests.Session = get_random_session()
        # if the session has no headers, we assume it is a new session and set the header
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if enable_agent:
            for k, v in agents.get_header().items():
                kwargs["headers"][k] = v
        if enable_proxy:
            kwargs["proxies"] = proxy_manager.get_proxy()
        response = None
        try:
            if goto_main_first_to_get_session_cookies and not session.cookies:
                # if we need to get session cookies, we go to the main page first
                main_url = "/".join(url.split("/")[:3])
                for i in range(3):
                    try:
                        session.get(main_url, timeout=3)
                        break
                    except Exception:
                        time.sleep(1)
            response = session.get(url, *args, **kwargs, timeout=timeout)
            if retry_on_status:
                response.raise_for_status()  # Raise an error for bad status codes
            return response
        except requests.RequestException as e:

            retries += 1
            if retries >= max_of_retries and max_of_retries >= 0:
                raise e
            else:
                time.sleep(sleep_between_retries)
  

def post(url, data=None, json=None, max_of_retries=3, timeout=2, sleep_between_retries=0.3, retry_on_status=False, enable_agent=True, enable_proxy=False, *args, **kwargs):
    """
    Makes a POST request to the specified URL using a random user agent and a proxy.
    """
    retries = 0
    while True:
        session: requests.Session = get_random_session()
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        if enable_agent:
            for k, v in agents.get_header().items():
                kwargs["headers"][k] = v
        if enable_proxy:
            kwargs["proxies"] = proxy_manager.get_proxy()
        response = None
        try:
            response = session.post(url, data=data, json=json, *args, **kwargs, timeout=timeout)
            if retry_on_status:
                response.raise_for_status()
            return response
        except requests.RequestException as e:
            retries += 1
            if retries >= max_of_retries and max_of_retries >= 0:
                raise e
            else:
                time.sleep(sleep_between_retries)


# test
if __name__ == "__main__":
    test_url = "http://api.ipify.org?format=json"
    response = get(test_url)
    response_basic = requests.get(test_url)
    if response:
        print(f"Response from {test_url}: {response.json()}")
        print(f"Basic Response from {test_url}: {response_basic.json()}")
    else:
        print("Failed to fetch the URL.")