with open("proxquest/user-agents.txt", "r") as f:
    useragents = f.readlines()
    useragents = [p.strip() for p in useragents]
    useragents = [x for x in useragents if x != ""]
    useragents = [x for x in useragents if x != "\n"]
    useragents = [x for x in useragents if x != "\r"]

import random
from itertools import cycle

random.shuffle(useragents)
cyc = cycle(useragents)

def get_header():
    return {"User-Agent":random.choice(useragents),"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}

def get_random_user_agent():
    return next(cyc)