# -*- coding:utf-8 -*-
'''
Yahoo Market Data API wrappers
'''
from __future__ import print_function
import urllib
import urllib2
from datetime import datetime


def fetch_market_data(symbol, from_date, to_date):
    '''
    Fetch yahoo market data for a specific symbol.
    Returns array of data which includes: 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'.
    '''
    try:
        params = urllib.urlencode({'a': from_date.month - 1, 'b': from_date.day, 'c': from_date.year, 'd': to_date.month - 1, 'e': to_date.day, 'f': to_date.year, 's': symbol})
        url_get = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?%s' % params)
        url_get.readline()  # skip csv header
        data = [url_get.readline()]
        while (len(data[-1]) > 0):
            data.append(url_get.readline())
        data = [[x.replace('\n', '') for x in l.split(',')] for l in data if len(l) > 0]
        data = [(datetime.strptime(x[0], '%Y-%m-%d'), float(x[1]), float(x[2]), float(x[3]), float(x[4]), int(x[5]), float(x[6])) for x in data]
        return (True, data)
    except Exception as e:
        print(e)
        return (False, e)
