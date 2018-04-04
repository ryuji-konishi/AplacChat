import sys
sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import parsers.ParserAtomic as pat
import parsers.ParserAtomicHeaderBody as pah
import parsers.ParserHeaderBody as phb
import utils.DataStore as ds
import utils.utils as utils

class TestAtomicParser(unittest.TestCase):
    def setUp(self):
        self.html = ('<html><head><title>test</title></head>'
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
            'test\nヘ ッ ダ ー 1\nこ ん に ち は 。\n',
            'ヘ ッ ダ ー 1\nこ ん に ち は 。\nさ よ う な ら 。\n'
            ]]
        self.assertCountEqual(expected, result_store.data)

class TestAtomicHeaderBodyParser(unittest.TestCase):
    def setUp(self):
        self.htmlStruct = ('<html><head><title>test</title></head>'
            '<body>'
            '<h4>H4-A</h4>'
            '<p>body H4-A-1</p>'
            '<h1>H1-A</h1>'
            '<p>body H1-A-1</p>'
            '<h3>H3-A</h3>'
            '<p>body H3-A-1</p>'
            '<h2>H2-A</h2>'
            '<p>body H2-A-1</p>'
            '<h1>H1-B</h1>'
            '<p>body H1-B-1</p>'
            '</body></html>')
        self.htmlHNest = ('<html><head><title>test</title></head>'
            '<body>'
            '<h1><span>Span1 within H1</span><span>Span2 within H1</span> and some text</h1>'
            '<p>body H1</p>'
            '</body></html>')
        
    def test_TreeParser(self):
        """Test the base class of admic parser. Dump the constructed tree into text and check it."""

        # Basic structure
        parser = pah.TreeParser()
        parser.feed(self.htmlStruct)
        expected = (
            'Root\n'
            ' test\n'
            ' h4 H4-A\n'
            '  body H4-A-1\n'
            ' h1 H1-A\n'
            '  body H1-A-1\n'
            '  h3 H3-A\n'
            '   body H3-A-1\n'
            '  h2 H2-A\n'
            '   body H2-A-1\n'
            ' h1 H1-B\n'
            '  body H1-B-1\n'
        )
        self.assertTrue(expected == parser.dump())

        # Nested elements in header
        parser = pah.TreeParser()
        parser.feed(self.htmlHNest)
        expected = (
            'Root\n'
            ' test\n'
            ' h1 Span1 within H1 Span2 within H1 and some text\n'
            '  body H1\n'
        )
        self.assertTrue(expected == parser.dump())

    def test_AtomicHeaderBodyParser(self):
        """Test the targetted atomic parser which is going to be in the actual use."""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = pah.Parser(result_store)
        parser.parse(self.htmlStruct)

        expected = [[
            'H 4 - A\nH 1 - A\nH 1 - A\nH 1 - A\nH 3 - A\nH 2 - A\nH 1 - B\n',
            'body H 4 - A - 1\nbody H 1 - A - 1\nH 3 - A\nH 2 - A\nbody H 3 - A - 1\nbody H 2 - A - 1\nbody H 1 - B - 1\n'
            ]]
        self.assertCountEqual(expected, result_store.data)

    def test_AtomicHeaderBodyParserJpn(self):
        """Test the targetted atomic parser with Japanese sentence."""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = pah.Parser(result_store)
        html = ('<html><head><title>test</title></head>'
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
        self.htmlStruct = ('<html><head><title>test</title></head>'
            '<body>'
            '<h1>H1-A</h1>'
            '<p>body H1-A-1</p>'
            '<h2>H2-A</h2>'
            '<p>body H2-A-1</p>'
            '<h2>H2-B</h2>'
            '<p>body H2-B-1</p>'
            '<p>body H2-B-2</p>'
            '<h3>H3-A</h3>'
            '<p>body H3-A-1</p>'
            '<h2>H2-C</h2>'
            '<p>body H2-C-1</p>'
            '<h1>H1-B</h1>'
            '<h3>H3-A</h3>'
            '<p>body H3-A-1</p>'
            '<h2>H2-A</h2>'
            '<p>body H2-A-1</p>'
            '</body></html>')
        
    def test_parse_h1(self):
        """Test H1"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store, 'h1')
        parser.parse(self.htmlStruct)

        expected = [
            ['H 1 - A\n', 'body H 1 - A - 1 <br> body H 2 - A - 1 <br> body H 2 - B - 1 <br> body H 2 - B - 2 <br> body H 3 - A - 1 <br> body H 2 - C - 1\n'],
            ['H 1 - B\n', 'body H 3 - A - 1 <br> body H 2 - A - 1\n']
            ]
        self.assertCountEqual(expected, result_store.data)

    def test_parse_h2(self):
        """Test H2"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store, 'h2')
        parser.parse(self.htmlStruct)

        expected = [
            ['H 2 - A\n', 'body H 2 - A - 1\n'],
            ['H 2 - B\n', 'body H 2 - B - 1 <br> body H 2 - B - 2 <br> body H 3 - A - 1\n'],
            ['H 2 - C\n', 'body H 2 - C - 1\n'],
            ['H 2 - A\n', 'body H 2 - A - 1\n']
            ]
        self.assertCountEqual(expected, result_store.data)

    def test_parse_h3(self):
        """Test H3"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store, 'h3')
        parser.parse(self.htmlStruct)

        expected = [
            ['H 3 - A\n', 'body H 3 - A - 1\n'],
            ['H 3 - A\n', 'body H 3 - A - 1\n']
            ]
        self.assertCountEqual(expected, result_store.data)

    def test_parse_script(self):
        """Test script element within a font element"""
        vocab = ds.VocabStore()
        result_store = ds.ParseResultStore(vocab)
        parser = phb.Parser(result_store)

        html = ('<html><head><title>test</title></head>'
            '<body>'
            '<h1>H1-A</h1>'
            '<font>font element body'
            '<script>script shouldn\'t be parsed</script>'
            '</font>'
            '</body></html>')

        parser.parse(html)

        expected = [
            ['H 1 - A\n', 'font element body\n'],
            ]
        self.assertCountEqual(expected, result_store.data)


if __name__ == "__main__":
    unittest.main()

