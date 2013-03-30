# -*- coding:utf-8 -*-
'''
Market data update functionality
'''
from __future__ import print_function
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import schema
from schema import Symbol, HistoricalPrice
import yahoo


def _parse_date(date):
    pass


def update_marketdata():
    session = sessionmaker(bind=schema.engine).Session()
    symbols = session.query(Symbol)
    from_date = datetime.now() - timedelta(days=365)  # TODO: change this later
    to_date = datetime.now() + timedelta(days=2)  # use a future date since there might be issues with timezones
    for symbol in symbols:
        (res, data) = yahoo.fetch_market_data(symbol, from_date, to_date)
        if res:
            session.add_all([HistoricalPrice(x[0], symbol, x[1], x[2], x[3], x[4], x[5], x[6]) for x in data])
            session.commit()
        else:
            print('Failed updating symbol %s' % symbol)


    # 2. get latest data from DB
    # 3. fetch required data from yahoo
    # 4. put data to DB
