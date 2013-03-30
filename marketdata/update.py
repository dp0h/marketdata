# -*- coding:utf-8 -*-
'''
Market data update functionality
'''
from sqlalchemy.orm import sessionmaker
import datetime as dt
import schema
from schema import Symbol
import yahoo


def update_marketdata():
    session = sessionmaker(bind=schema.engine).Session()
    symbols = session.query(Symbol)
    from_date = dt.datetime.now() - dt.timedelta(days=365)  # TODO: change this later
    to_date = dt.datetime.now() + dt.timedelta(days=2)  # use a future date since there might be issues with timezones
    for x in symbols:
        res = yahoo.fetch_market_data(symbol, from_date, to_date)
        print (res)
        pass


    # 2. get latest data from DB
    # 3. fetch required data from yahoo
    # 4. put data to DB
    pass
