# -*- coding:utf-8 -*-
'''
Market data access functionality
'''
from __future__ import print_function
from sqlalchemy.orm import sessionmaker
import schema
from schema import HistoricalPrice
import numpy
import pandas


class Column:
    Open = HistoricalPrice.open
    High = HistoricalPrice.high
    Low = HistoricalPrice.low
    Close = HistoricalPrice.close
    Volume = HistoricalPrice.volume
    AdjClose = HistoricalPrice.adj_close


def get_marketdata(symbol, from_date, to_date, columns):
    '''
    Retrieve market data for specific symbol
    '''
    session = sessionmaker(bind=schema.engine)()
    query_result = session.query(*([HistoricalPrice.date] + columns)).\
        filter(HistoricalPrice.symbol == symbol).\
        filter(HistoricalPrice.date >= from_date).\
        filter(HistoricalPrice.date <= to_date)
    data = None
    dates = []
    for x in query_result:
        dates.append(x[0])
        data = numpy.vstack([data, x[1:]]) if data is not None else numpy.array(x[1:])
    return pandas.DataFrame(data, index=dates)
