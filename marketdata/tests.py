#!/usr/bin/env python
# coding: utf-8

import unittest
from test import test_support
from symbols import add_symbols, remove_symbols, symbols, clean_symbols


class TestSymbols(unittest.TestCase):
    def setUp(self):
        clean_symbols()

    def test_clean(self):
        add_symbols(['AAPL'])
        clean_symbols()
        act = symbols()
        self.assertEquals(0, len(act))

    def test_add(self):
        exp = ['AAPL']
        add_symbols(exp)
        act = [x['_id'] for x in symbols()]
        self.assertListEqual(exp, act)

    def test_remove(self):
        exp = ['AAPL']
        added = ['MSFT']
        add_symbols(exp + added)
        remove_symbols(added)
        act = [x['_id'] for x in symbols()]
        self.assertListEqual(exp, act)


if __name__ == '__main__':
    test_support.run_unittest(TestSymbols)
