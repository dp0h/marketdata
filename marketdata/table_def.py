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
    name = Column(String)

    def __init__(self, name):
        self.name = name


class HistoricalPrice(Base):
    __tablename__ = 'historical_prices'
    date = Column(DateTime)
    symbol = Column(String)
    open = Column(Numeric(12, 2))
    high = Column(Numeric(12, 2))
    low = Column(Numeric(12, 2))
    close = Column(Numeric(12, 2))
    volume = Column(Integer)
    adj_close = Column(Numeric(12, 2))


def create_all():
    Base.metadata.create_all(engine)
