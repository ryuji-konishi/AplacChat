# -*- coding: utf-8 -*-
import sys
# Windows
# sys.path.insert(0, '..\\')  # This is required to import common
# Mac/Linux
sys.path.insert(0, '..//')  # This is required to import common

import unittest
import ParserAtomic as pat
import ParserAtomicHeaderBody as pah
import ParserHeaderBody as phb
import DataStore as ds
import utils.utils as utils

class TestAtomicParser(unittest.TestCase):
    def setUp(self):
        self.html = ('<html><head><title>Test</title></head>'
            '<body>'
            '<h1>ヘッダー1</h1>'
            '<p>こんにちは。さようなら。</p>'
            '</body></html>')
        
    def test_AtomicParserJpn(self):
        """Test the targetted atomic parser with Japanese sentence."""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = pat.Parser(result_store)
        parser.parse(self.html)

        expected = [[
            'Test\nヘ ッ ダ ー 1\nこ ん に ち は 。\n',
            'ヘ ッ ダ ー 1\nこ ん に ち は 。\nさ よ う な ら 。\n'
            ]]
        self.assertCountEqual(expected, result_store.data)

class TestAtomicHeaderBodyParser(unittest.TestCase):
    def setUp(self):
        self.html = ('<html><head><title>Test</title></head>'
            '<body>'
            '<h4>H4-A</h4>'
            '<p>Body H4-A-1</p>'
            '<h1>H1-A</h1>'
            '<p>Body H1-A-1</p>'
            '<h3>H3-A</h3>'
            '<p>Body H3-A-1</p>'
            '<h2>H2-A</h2>'
            '<p>Body H2-A-1</p>'
            '<h1>H1-B</h1>'
            '<p>Body H1-B-1</p>'
            '</body></html>')
        
    def test_TreeParser(self):
        """Test the base class of admic parser. Dump the constructed tree into text and check it."""
        parser = pah.TreeParser()
        parser.feed(self.html)
        expected = (
            'Root\n'
            ' h4 H4-A\n'
            '  Body H4-A-1\n'
            ' h1 H1-A\n'
            '  Body H1-A-1\n'
            '  h3 H3-A\n'
            '   Body H3-A-1\n'
            '  h2 H2-A\n'
            '   Body H2-A-1\n'
            ' h1 H1-B\n'
            '  Body H1-B-1\n'
        )
        self.assertTrue(expected == parser.dump())

    def test_AtomicHeaderBodyParser(self):
        """Test the targetted atomic parser which is going to be in the actual use."""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = pah.Parser(result_store)
        parser.parse(self.html)

        expected = [[
            'H4-A\nH1-A\nH1-A\nH1-A\nH3-A\nH2-A\nH1-B\n',
            'Body H4-A-1\nBody H1-A-1\nH3-A\nH2-A\nBody H3-A-1\nBody H2-A-1\nBody H1-B-1\n'
            ]]
        self.assertCountEqual(expected, result_store.data)

    def test_AtomicHeaderBodyParserJpn(self):
        """Test the targetted atomic parser with Japanese sentence."""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = pah.Parser(result_store)
        html = ('<html><head><title>Test</title></head>'
            '<body>'
            '<h1>ヘッダー1</h1>'
            '<p>こんにちは。さようなら。</p>'
            '</body></html>')
        parser.parse(html)

        expected = [[
            'ヘ ッ ダ ー 1\nヘ ッ ダ ー 1\n',
            'こ ん に ち は 。\nさ よ う な ら 。\n'
            ]]
        self.assertCountEqual(expected, result_store.data)

class TestHeaderBodyParser(unittest.TestCase):
    def setUp(self):
        self.html = ('<html><head><title>Test</title></head>'
            '<body>'
            '<h1>H1-A</h1>'
            '<p>Body H1-A-1</p>'
            '<h2>H2-A</h2>'
            '<p>Body H2-A-1</p>'
            '<h2>H2-B</h2>'
            '<p>Body H2-B-1</p>'
            '<p>Body H2-B-2</p>'
            '<h3>H3-A</h3>'
            '<p>Body H3-A-1</p>'
            '<h2>H2-C</h2>'
            '<p>Body H2-C-1</p>'
            '<h1>H1-B</h1>'
            '<h3>H3-A</h3>'
            '<p>Body H3-A-1</p>'
            '<h2>H2-A</h2>'
            '<p>Body H2-A-1</p>'
            '</body></html>')
        
    def test_parse_h1(self):
        """Test H1"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store, 'h1')
        parser.parse(self.html)

        expected = [
            ['H1-A\n', 'Body H1-A-1 <br> Body H2-A-1 <br> Body H2-B-1 <br> Body H2-B-2 <br> Body H3-A-1 <br> Body H2-C-1\n'],
            ['H1-B\n', 'Body H3-A-1 <br> Body H2-A-1\n']
            ]
        self.assertCountEqual(expected, result_store.data)

    def test_parse_h2(self):
        """Test H2"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store, 'h2')
        parser.parse(self.html)

        expected = [
            ['H2-A\n', 'Body H2-A-1\n'],
            ['H2-B\n', 'Body H2-B-1 <br> Body H2-B-2 <br> Body H3-A-1\n'],
            ['H2-C\n', 'Body H2-C-1\n'],
            ['H2-A\n', 'Body H2-A-1\n']
            ]
        self.assertCountEqual(expected, result_store.data)

    def test_parse_h3(self):
        """Test H3"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store, 'h3')
        parser.parse(self.html)

        expected = [
            ['H3-A\n', 'Body H3-A-1\n'],
            ['H3-A\n', 'Body H3-A-1\n']
            ]
        self.assertCountEqual(expected, result_store.data)

class TestResultStore(unittest.TestCase):
    def setUp(self):
        pass

    def test_store_result(self):
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)

        # If the input to the result store is either
        # - a line of text or
        # - a list of text
        # the result will be the same shaped list of text.
        result_store.store_result('source text', 'target text')
        self.assertTrue(
            result_store.data, 
            ['source text\n', 'target text\n'])
        result_store.clear()

        result_store.store_result(['source text'], ['target text'])
        self.assertTrue(
            result_store.data, 
            ['source text\n', 'target text\n'])
        result_store.clear()

        # The result is broken into multiple lines if multiple inputs are stored.
        result_store.store_result(['source text1', 'source text2'], ['target text1', 'target text2'])
        self.assertTrue(
            result_store.data, 
            ['source text1\nsource text2\n', 'target text1\ntarget text2\n'])
        result_store.clear()

        # The result is broken into words space ' ' separated.
        # If the input text is multi-byte character, each character is separated.
        result_store.store_result(['source text', 'ソース'], ['target text', 'ターゲット'])
        self.assertTrue(
            result_store.data, 
            ['source text\nソ ー ス\n', 'target text\nタ ー ゲ ッ ト\n'])
        result_store.clear()

        # The input is single line of source and multi lines of target.
        result_store.store_result('source line', 'target line1\ntarget line2')
        self.assertTrue(
            result_store.data, 
            ['source line\n', 'target line <br> target line2\n'])
        result_store.clear()


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_trim_structural_char(self):
        self.assertTrue(utils.trim_structural_char('') == '')
        self.assertTrue(utils.trim_structural_char(' ') == '')
        self.assertTrue(utils.trim_structural_char('  ') == '')
        self.assertTrue(utils.trim_structural_char(' a ') == 'a')
        self.assertTrue(utils.trim_structural_char('　') == '')
        self.assertTrue(utils.trim_structural_char('　　') == '')
        self.assertTrue(utils.trim_structural_char('　a　') == 'a')
        self.assertTrue(utils.trim_structural_char('\n') == '')
        self.assertTrue(utils.trim_structural_char('\n\n') == '')
        self.assertTrue(utils.trim_structural_char('\na\n') == 'a')
        self.assertTrue(utils.trim_structural_char('\t') == '')
        self.assertTrue(utils.trim_structural_char('\t\t') == '')
        self.assertTrue(utils.trim_structural_char('\ta\t') == 'a')


if __name__ == "__main__":
    unittest.main()

