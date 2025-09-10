# Idealo Item Crawler
Loads data from Idealo and put profitable amazon arbitrage deals to a google sheet

## Installation
1. Download Code from Github
2. `pip install -r requierements.txt`

## Setup
1. Add all Blacklisted words to backlist.txt (use linebreak)
1. Add all Blacklisted brands to marken_blacklist.txt (use linebreak)
1. Add all Blacklisted shops to shop_blacklist.txt (use linebreak)
1. Auth your google project, add google drive and google tables add the client_secret.json file to the project root
1. You can change the ids of the scanned shops in the main.py file

## Start
1. `python main.py`
