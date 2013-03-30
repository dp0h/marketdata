# -*- coding:utf-8 -*-
'''
Yahoo Market Data API wrappers
'''
import urllib
import urllib2


def fetch_market_data(symbol, from_date, to_date):
    try:
        params = urllib.urlencode({'a': from_date.month - 1, 'b': from_date.day, 'c': from_date.year, 'd': to_date.month - 1, 'e': to_date.day, 'f': to_date.year, 's': symbol})
        url_get = urllib2.urlopen('http://ichart.finance.yahoo.com/table.csv?%s' % params)
        header = url_get.readline()
        data = [url_get.readline()]
        while (len(data[-1]) > 0):
            data.append(url_get.readline())
        data = [x for x in data if len(x) > 0]
        #  TODO: parse the date and return as a numpy.array
        return (True, (header, data))
    except urllib2.HTTPError:
        return (False, None)
    except urllib2.URLError:
        return (False, None)
