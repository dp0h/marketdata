#!/usr/bin/env python
# coding: utf-8

import unittest
from test import test_support
import pymongo
from datetime import datetime
from symbols import Symbols
from yahoo import fetch_market_data
from update import update_marketdata


class TestSymbols(unittest.TestCase):
    def setUp(self):
        self.symbols = Symbols()

        conn = pymongo.MongoClient()
        db = conn.test_marketdata
        symbols = db.test_symbols

        self.symbols._symbols = symbols  # replaces real db with test one
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


class TestMarketDataDb(unittest.TestCase):
    def setUp(self):
        self.symbols = Symbols()

        conn = pymongo.MongoClient()
        db = conn.test_marketdata
        symbols = db.test_symbols

        self.symbols._symbols = symbols  # replaces real db with test one
        self.symbols.clean()
        self.symbols.add(['AAPL'])

    def test_single_hist_price(self):
        dt = datetime(2013, 7, 13)
        self.symbols.insert_historical_prices('AAPL', [(dt, 100.0, 101.0, 99.0, 100.0, 100, 100.0)])
        res = self.symbols.select_historical_prices('AAPL', dt, dt)
        self.assertEqual(1, len(res))
        self.assertEqual(dt, res[0]['date'])
        self.assertEqual(100.0, res[0]['open'])
        self.assertEqual(101.0, res[0]['high'])
        self.assertEqual(99.0, res[0]['low'])
        self.assertEqual(100.0, res[0]['close'])
        self.assertEqual(100, res[0]['volume'])
        self.assertEqual(100.0, res[0]['adj_close'])

    def test_hist_price_for_undefined_date(self):
        dt = datetime(2013, 7, 13)
        res = self.symbols.select_historical_prices('AAPL', dt, dt)
        self.assertEqual([], res)

    def test_three_hist_price(self):
        d1 = datetime(2013, 7, 13)
        d2 = datetime(2013, 7, 14)
        d3 = datetime(2013, 7, 15)
        self.symbols.insert_historical_prices('AAPL', [(d1, 100.0, 101.0, 99.0, 100.0, 100, 100.0)])
        self.symbols.insert_historical_prices('AAPL', [(d3, 99.0, 100.0, 98.0, 99.0, 99, 99.0)])
        self.symbols.insert_historical_prices('AAPL', [(d2, 101.0, 102.0, 100.0, 101.0, 101, 101.0)])
        res = self.symbols.select_historical_prices('AAPL', d1, d3)
        self.assertEqual(3, len(res))
        self.assertEqual(d1, res[0]['date'])
        self.assertEqual(100.0, res[0]['open'])
        self.assertEqual(d2, res[1]['date'])
        self.assertEqual(101.0, res[1]['open'])
        self.assertEqual(d3, res[2]['date'])
        self.assertEqual(99.0, res[2]['open'])

    def test_date_filtering(self):
        d1 = datetime(2013, 7, 13)
        d2 = datetime(2013, 7, 14)
        d3 = datetime(2013, 7, 15)
        d4 = datetime(2013, 7, 16)
        self.symbols.insert_historical_prices('AAPL', [(d1, 100.0, 101.0, 99.0, 100.0, 100, 100.0)])
        self.symbols.insert_historical_prices('AAPL', [(d2, 101.0, 102.0, 100.0, 101.0, 101, 101.0)])
        self.symbols.insert_historical_prices('AAPL', [(d3, 99.0, 100.0, 98.0, 99.0, 99, 99.0)])
        self.symbols.insert_historical_prices('AAPL', [(d4, 98.0, 99.0, 97.0, 98.0, 98, 98.0)])
        res = self.symbols.select_historical_prices('AAPL', d2, d3)
        self.assertEqual(2, len(res))
        self.assertEqual(d2, res[0]['date'])
        self.assertEqual(101.0, res[0]['open'])
        self.assertEqual(d3, res[1]['date'])
        self.assertEqual(99.0, res[1]['open'])

    def test_reinsert_historical_prices(self):
        d1 = datetime(2013, 7, 13)
        d2 = datetime(2013, 7, 14)
        d3 = datetime(2013, 7, 15)
        self.symbols.insert_historical_prices('AAPL', [(d1, 100.0, 101.0, 99.0, 100.0, 100, 100.0), (d2, 101.0, 102.0, 100.0, 101.0, 101, 101.0), (d3, 99.0, 100.0, 98.0, 99.0, 99, 99.0)])
        res = self.symbols.select_historical_prices('AAPL', d1, d3)
        self.assertEqual(3, len(res))
        self.symbols.insert_historical_prices('AAPL', [(d2, 101.0, 102.0, 100.0, 101.0, 101, 101.0)])
        res = self.symbols.select_historical_prices('AAPL', d1, d3)
        self.assertEqual(3, len(res))
        self.assertEqual(d1, res[0]['date'])
        self.assertEqual(100.0, res[0]['open'])
        self.assertEqual(d2, res[1]['date'])
        self.assertEqual(101.0, res[1]['open'])
        self.assertEqual(d3, res[2]['date'])
        self.assertEqual(99.0, res[2]['open'])

    def test_last_date(self):
        d = [datetime(2013, 7, 16), datetime(2013, 7, 14), datetime(2013, 7, 13),  datetime(2013, 7, 17), datetime(2013, 7, 12),  datetime(2013, 7, 15)]
        for x in d:
            self.symbols.insert_historical_prices('AAPL', [(x, 1.0, 1.0, 1.0, 1.0, 1, 1.0)])
        res = self.symbols.last_date('AAPL')
        self.assertEquals(datetime(2013, 7, 17), res)

    def test_last_date_when_no_data(self):
        res = self.symbols.last_date('AAPL')
        self.assertEquals(None, res)


class UpdateMarketDataIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.symbols = Symbols()

        conn = pymongo.MongoClient()
        db = conn.test_marketdata
        symbols = db.test_symbols

        self.symbols._symbols = symbols  # replaces real db with test one
        self.symbols.clean()
        self.symbols.add(['AAPL'])

    def test_update_marketdata(self):
        from_date = datetime(2012, 9, 20)
        to_date = datetime(2012, 9, 21)
        update_marketdata(from_date, to_date, self.symbols)

        res = self.symbols.select_historical_prices('AAPL', from_date, to_date)
        self.assertEqual(2, len(res))
        self.assertEqual(from_date, res[0]['date'])
        self.assertEqual(705.07, res[0]['high'])
        self.assertEqual(to_date, res[1]['date'])
        self.assertEqual(705.07, res[1]['high'])


if __name__ == '__main__':
    test_support.run_unittest(TestSymbols)
    test_support.run_unittest(YahooIntegrationTest)
    test_support.run_unittest(TestMarketDataDb)
    test_support.run_unittest(UpdateMarketDataIntegrationTest)
