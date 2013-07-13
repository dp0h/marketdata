# coding:utf-8
'''
Functions working with symbols
'''

import pymongo


class Symbols(object):
    def __init__(self):
        self._conn = pymongo.MongoClient()
        self._db = self._conn.marketdata
        self._symbols = self._db.symbols

    def add(self, symbols):
        for s in symbols:
            self._symbols.insert({'_id': s, 'mdata': []})

    def remove(self, symbols):
        for s in symbols:
            self._symbols.remove({'_id': s})

    def symbols(self):
        return [x for x in self._symbols.find({}, {'_id': 1})]

    def clean(self):
        self._symbols.drop()

    def insert_historical_prices(self, symbol, data):
        '''
        data should have such format [(datetime, open , high, low, close, volume, adj_close)]
        '''
        mdata = [{'_id': x[0], 'open': x[1], 'high': x[2], 'low': x[3], 'close': x[4], 'volume': x[5], 'adj_close': x[6]} for x in data]
        print(mdata)
        self._symbols.update({'_id': symbol}, {'$addToSet': {'mdata': mdata}})

    def select_historical_prices(self, symbol, from_date, to_date):
        '''
        result has the following format [{'_id': date, 'open': open, ...}]
        '''
        res = self._symbols.aggregate([
            {'$match': {'_id': symbol}},
            {'$unwind': '$mdata'},
            {'$match': {'mdata._id': {'$gte': from_date, '$lte': to_date}}},
            {'$sort': {'mdata._id': 1}}
        ])
        print(res)
        return [x['mdata'][0] for x in res['result']]
