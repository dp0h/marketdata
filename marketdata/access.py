# coding:utf-8
'''
Market data access functionality
'''
from __future__ import print_function
from symbols import Symbols


def get_marketdata(symbol, from_date, to_date):
    '''
    Retrieve market data for specific symbol
    '''
    return Symbols().select_historical_prices(symbol, from_date, to_date)
