import random

useragents = []
try:
    with open("headers.txt") as f:
        for l in f:
            useragents.append(l.replace("\n", ""))
except:
    with open("item_filter/headers.txt") as f:
        for l in f:
            useragents.append(l.replace("\n", ""))



basic_header = """Host: sellercentral.amazon.de
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: de,en-US;q=0.7,en;q=0.3
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
Cookie: session-id=258-3718040-0907025; ubid-acbde=261-3587442-8049905; session-token=mSDQYhXX9hZE+i7ehYj1c83pOueqOS0jVk8LI8YM09XcF5pG/JJHOXCSNWKs6ikgGwLmEwjncF03iIsxeoNOzv+/zPsf8Toy+N/fjVcXbOxlwaT74U6qpSTinZ2g8thb+p9G9TQHHMpllGvw5GAFqgOciqG7MxbZwXmwR/PwuVanpM8eiAbhwLcwh1FchQ3jfTHDcmgYOtTKA8POZPw7YjF5361FXreDui9Pk5N7w21NMwTuTYqqR/d3Z6JlmOtZFFM8ROj3bTq9BlXi0/tWsbrDBp1egM4MHuSPnpobVcs4gXgpxJ3JDZEkmZ9DP1Id7j6mzJeZParB1gEw0fPzmfwPkOzb/0EQ
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Sec-GPC: 1
TE: trailers"""

def_header = {}

for l in basic_header.split("\n"):
    k, v = l.split(": ")
    def_header[k] = v
    

def get_header():
    def_header["User-Agent"] = get_random_user_agent()
    return def_header

def get_random_user_agent():
    return random.choice(useragents)