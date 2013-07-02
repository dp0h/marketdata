# -*- coding:utf-8 -*-
'''
Functions working with symbols
'''
from sqlalchemy.orm import sessionmaker
import schema
from schema import Symbol, HistoricalPrice


def add_symbols(symbols):
    session = sessionmaker(bind=schema.engine)()
    session.add_all([Symbol(x) for x in symbols])
    session.commit()


def remove_symbols(symbols):
    session = sessionmaker(bind=schema.engine)()
    for x in symbols:
        session.query(Symbol).filter_by(name = x).delete()
        session.query(HistoricalPrice).filter_by(symbol = x).delete()
    session.commit()


def symbols():
    session = sessionmaker(bind=schema.engine)()
    for s in session.query(Symbol):
        yield s.name
