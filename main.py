#!/bin/python
import requests
import bs4
import sys
from tqdm import tqdm
import os
import json


config = json.loads(open(os.path.join(sys.path[0], 'eastcoastlifestyle.json')).read())
BASE_URL = config['BASE_URL']
COLLECTIONS_ALL_URL = BASE_URL + '/collections/all/'
PAGINATOR_SELECTOR = config['PAGINATOR_SELECTOR']
ITEM_DETAIL_SELECTOR = config['ITEM_DETAIL_SELECTOR']
ITEM_IMAGE_SELECTOR = config['ITEM_IMAGE_SELECTOR']
ITEM_TITLE_SELECTOR = config['ITEM_TITLE_SELECTOR']
ITEM_PRICE_SELECTOR = config['ITEM_PRICE_SELECTOR']


def getImageUrl(soup, selector):
    imageTags = soup.select(selector)

    return 'https:' + imageTags[0].get('data-original-src')


def getText(soup, selector):
    tags = soup.select(selector)

    return tags[0].getText()


def getItemDetails(urls):
    itemDetails = dict()
    print('Grabbing item details...')
    for url in tqdm(urls):
        soup = getResource(url)
        imageUrl = getImageUrl(soup, ITEM_IMAGE_SELECTOR)
        title = getText(soup, ITEM_TITLE_SELECTOR)
        price = getText(soup, ITEM_PRICE_SELECTOR)
        itemDetails[title] = {'imageUrl': imageUrl, 'price': price}

    return itemDetails
  

def getResource(url):
    """Take a URL and return a soup object"""
    response = requests.get(url)
    try:
        response.raise_for_status()
    except:
        print('Invalid URL')
        sys.exit()

    return bs4.BeautifulSoup(response.text, features='lxml')


def getAllPages(baseUrl, selector):
    """Get pages"""
    soup = getResource(baseUrl)

    individualPageUrls = []
    for url in soup.select(selector):
        individualPageUrls.append(url.get('href'))

    individualPageUrls = individualPageUrls[:-1]
    individualPageUrls = [url.split('all')[-1] for url in individualPageUrls]
    individualPageUrls = [baseUrl + url for url in individualPageUrls]
    individualPageUrls.append(baseUrl)

    return individualPageUrls


def getAllItems(baseUrl, addresses, selector):
    allItems = []
    print('Grabbing item detail pages...')
    for url in tqdm(addresses):
        soup = getResource(url)
        stubs = []
        for itemUrl in soup.select(selector):
            stubs.append(itemUrl.get('href'))
        stubs = [baseUrl + stub for stub in stubs]
        allItems.extend(stubs)
    
    return allItems


if __name__ == '__main__':
    allPages = getAllPages(COLLECTIONS_ALL_URL, PAGINATOR_SELECTOR)
    allItems = getAllItems(BASE_URL, allPages, ITEM_DETAIL_SELECTOR)
    itemDetails = getItemDetails(allItems)
    jsonDump = json.dumps(itemDetails, indent=4)
    print('Writing to database.json')
    with open('database.json', 'w') as f:
        f.write(jsonDump)

    print('Complete')