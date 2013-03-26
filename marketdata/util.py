# -*- coding:utf-8 -*-
'''
Utility functions
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import Symbol


def add_symbols(symbols):
    engine = create_engine('sqlite:///marketdata.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add_all([Symbol(x) for x in symbols])
    session.commit()
