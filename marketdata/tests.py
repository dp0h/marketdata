#!/usr/bin/env python
# coding: utf-8

import unittest
from test import test_support
from symbols import Symbols
import pymongo


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


if __name__ == '__main__':
    test_support.run_unittest(TestSymbols)
