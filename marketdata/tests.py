#!/usr/bin/env python
# coding: utf-8

import unittest
from test import test_support
import pymongo
from symbols import Symbols
from yahoo import fetch_market_data
from datetime import datetime


class TestSymbols(unittest.TestCase):
    def setUp(self):
        self.symbols = Symbols()

        conn = pymongo.MongoClient()
        db = conn.test_marketdata
        symbols = db.test_symbols

        self.symbols._symbols = symbols  # replace real db with test one
        self.symbols.clean()

    def test_clean(self):
        self.symbols.add(['AAPL'])
        self.symbols.clean()
        act = self.symbols.symbols()
        self.assertEquals(0, len(act))

    def test_add(self):
        exp = ['AAPL']
        self.symbols.add(exp)
        act = [x['_id'] for x in self.symbols.symbols()]
        self.assertListEqual(exp, act)

    def test_remove(self):
        exp = ['AAPL']
        added = ['MSFT']
        self.symbols.add(exp + added)
        self.symbols.remove(added)
        act = [x['_id'] for x in self.symbols.symbols()]
        self.assertListEqual(exp, act)


class TestMarketDataDb(object):
    pass


class YahooIntegrationTest(unittest.TestCase):
    def test_AAPL_shares(self):
        from_date = datetime(2012, 9, 20)
        to_date = datetime(2012, 9, 21)
        res, data = fetch_market_data('AAPL', from_date, to_date)
        self.assertTrue(res)
        self.assertEqual(2, len(data))
        self.assertAlmostEquals(to_date, data[0][0])
        self.assertAlmostEquals(705.07, data[0][2])

    def test_unknown_symbol(self):
        res, _ = fetch_market_data('XXX', datetime(2012, 9, 20), datetime(2012, 9, 21))
        self.assertFalse(res)


if __name__ == '__main__':
    test_support.run_unittest(TestSymbols)
    test_support.run_unittest(YahooIntegrationTest)
