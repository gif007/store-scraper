#!/bin/python
import json
import sys
import os
from statistics import mean

db = json.loads(open(os.path.join(sys.path[0], 'database.json')).read())


def getMean(data):
    """Gets means price data from database.json"""
    prices = []
    for key in data.keys():
        prices.append(int(data[key]['price'].lstrip('$')))

    return round(mean(prices), 2)


if __name__ == '__main__':
    mean = getMean(db)
    print('The average cost of an item at this store is: $' + str(mean))