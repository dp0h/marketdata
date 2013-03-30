# -*- coding:utf-8 -*-
'''
Table definitions
'''
from sqlalchemy import create_engine
from sqlalchemy import Column, DateTime, Integer, String, Numeric
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///marketdata.db', echo=True)
Base = declarative_base()


class Symbol(Base):
    __tablename__ = 'symbols'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class HistoricalPrice(Base):
    __tablename__ = 'historical_prices'

    date = Column(DateTime, primary_key=True)
    symbol = Column(String, primary_key=True)
    open = Column(Numeric(12, 2))
    high = Column(Numeric(12, 2))
    low = Column(Numeric(12, 2))
    close = Column(Numeric(12, 2))
    volume = Column(Integer)
    adj_close = Column(Numeric(12, 2))

    def __init__(self, date, symbol, open, high, low, close, volume, adj_close):
        self.date = date
        self.symbol = symbol
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adj_close = adj_close


def create():
    Base.metadata.create_all(engine)
