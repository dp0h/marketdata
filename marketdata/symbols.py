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
