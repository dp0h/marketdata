# -*- coding:utf-8 -*-
'''
Utility functions
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schema import Symbol, HistoricalPrice


def _create_session():
    engine = create_engine('sqlite:///marketdata.db', echo=True)
    Session = sessionmaker(bind=engine)
    return Session()


def add_symbols(symbols):
    session = _create_session()
    session.add_all([Symbol(x) for x in symbols])
    session.commit()


def remove_symbols(symbols):
    session = _create_session()
    for x in symbols:
        session.query(Symbol).filter_by(name = x).delete()
        session.query(HistoricalPrice).filter_by(symbol = x).delete()
    session.commit()


def symbols():
    session = _create_session()
    for s in session.query(Symbol):
        yield s.name
