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
        sc.insert({'_id': s, 'mdata': []})


def remove_symbols(symbols):
    sc = __symbols_collection()
    for s in symbols:
        sc.remove({'_id': s})


def symbols():
    sc = __symbols_collection()
    return [x for x in sc.find({}, {'_id': 1})]


def clean_symbols():
    __symbols_collection().drop()
