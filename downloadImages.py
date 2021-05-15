#!/bin/python
import json
import sys
import os
from tqdm import tqdm
import requests

db = json.loads(open(os.path.join(sys.path[0], 'database.json')).read())

def createTuples(data):
    listofTuples = []
    for key in data.keys():
        oneTuple = (key, data[key]['imageUrl'])
        listofTuples.append(oneTuple)

    return listofTuples

def getResource(URL):
    """Takes a URL and attempts to return the HTTP response"""
    try:
        resource = requests.get(URL)
    except Exception as exc:
        print('[ERROR] %s\n' % exc)
        exit()

    try:
        resource.raise_for_status()
    except Exception as exc:
        print('[ERROR] %s\n' % exc)
        exit()

    return resource


def downloadImage(name, url):
    ''' Download the image at given URL'''
    openURL = getResource(url)

    if '/' in name:
        name = name.replace('/', ' or ')

    name = name.rstrip('\\')

    fileName = name + '.jpg'

    with open(fileName, 'wb') as file:
        for chunk in openURL.iter_content(100000):
            file.write(chunk)


if __name__ == '__main__':
    dirName = os.path.join(sys.path[0], 'database-images')

    if not os.path.isdir(dirName):
        os.mkdir(dirName)

    os.chdir(dirName)
    tuples = createTuples(db)

    for pair in tqdm(tuples):
        downloadImage(pair[0], pair[1])