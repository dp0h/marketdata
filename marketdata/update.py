# -*- coding:utf-8 -*-
'''
Market data update functionality
'''
from sqlalchemy.orm import sessionmaker
import schema
from schema import Symbol


def update_marketdata():
    session = sessionmaker(bind=schema.engine).Session()
    symbols = session.query(Symbol)
    for x in symbols:
        pass


    # 2. get latest data from DB
    # 3. fetch required data from yahoo
    # 4. put data to DB
    pass
