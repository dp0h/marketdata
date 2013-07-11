# coding:utf-8
'''
Functions working with symbols
'''

import pymongo


def __symbols_collection():
    conn = pymongo.MongoClient()
    db = conn.marketdata
    return db.symbols


def add_symbols(symbols):
    sc = __symbols_collection()
    for s in symbols:
        sc.insert({'_id': s})


def remove_symbols(symbols):
    # removing symbols should remove market data as well
    pass


def symbols():
    pass


def symbols_clean():
    # market_data should be removed as well
    pass
