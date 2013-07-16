# coding:utf-8
'''
Market data update functionality
'''
from __future__ import print_function
from datetime import datetime, timedelta
from symbols import Symbols
import yahoo


def update_marketdata(from_date=None, to_date=None, sym=Symbols()):
    '''
    Fetch latest market data and upate it in db
    '''
    for s in sym.symbols():
        if not from_date:
            from_date = datetime.now() - timedelta(days=10*365)  # fetch market data for 10 years
        if not to_date:
            to_date = datetime.now() + timedelta(days=2)  # use a future date since there might be issues with timezones
        date = sym.last_date(s)
        fdate = date + timedelta(days=1) if date is not None else from_date
        (res, data) = yahoo.fetch_market_data(s, fdate, to_date)
        if res:
            sym.insert_historical_prices(s, [(x[0], x[1], x[2], x[3], x[4], x[5], x[6]) for x in data])
        else:
            # There are several reasons update can fail: 1. No new data; 2. wrong symbol; 3. Other reason.
            print('Failed updating symbol %s' % s)
