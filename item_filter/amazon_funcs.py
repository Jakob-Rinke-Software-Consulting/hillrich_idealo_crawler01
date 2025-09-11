import json
import proxquest
import re

DIRCET_URL = "http://sellercentral.amazon.de/rcpublic/productmatch?searchKey={}&countryCode=DE&locale=de-DE"

def get_ean(url):
    match = re.search(r'/dp/([^/?]+)', url)
    if match:
        return match.group(1)
    else:
        return ""

def get_bsr(soup):
    try:
        return soup['salesRank']
    except:
        return -1

def get_rating_count(soup):
    try:
        return soup['customerReviewsCount']
    except:
        return -1

def get_rating(soup):
    try:
        return soup['customerReviewsRatingValue']
    except:
        return -1
    
def get_weights_kg(soup):
    try:
        unit = soup['weightUnit']
        weight = soup['weight']
        if unit == 'grams':
            return weight / 1000
        elif unit == "kilograms":
            return weight
    except:
        pass
    return -1

def get_dimensions_m3(soup):
    try:
        unit = soup['dimensionUnit']
        length = soup['length']
        width = soup['width']
        height = soup['height']
        if unit == 'centimeters':
            return (length / 100) * (width / 100) * (height / 100)
        elif unit == "meters":
            return length * width * height
    except:
        pass
    return -1

def get_kat_name(soup):
    try:
        return soup['salesRankContextName']
    except:
        return get_cat(soup)


def get_amazon_json(id):
    url = DIRCET_URL.format(id)
    try:
        content = proxquest.get(url, timeout=3, max_of_retries=3)
        content = content.text
    except Exception as e:
        return "{}"
    try:
        js = json.loads(content, strict=False)
    except Exception as e:
        js = {"succeed": False}

    if js.get('succeed', False) == False:
        return "{}"
    if len(js["data"]["otherProducts"]["products"]) == 0:
        return "{}"
    return js["data"]["otherProducts"]["products"][0]

def get_cat(soup):
    try:
        return soup['gl']
    except:
        return "gl_electronics"


if __name__ == '__main__':
    js = get_amazon_json('B09TPPRG8B')
    print(get_bsr(js))
    print(get_rating_count(js))
    print(get_cat(js))
    print(get_weights_kg(js))

    soup2 = get_amazon_json('B09H1KQ2DH')
    print(get_bsr(soup2))
    print(get_cat(soup2))
    print(get_weights_kg(soup2))