import sys
sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import parsers.ParserAtomic as pat
import parsers.ParserAtomicHeaderBody as pah
import parsers.ParserHeaderBody as phb
import utils.corpus_utils as corpus_utils
import utils.vocab_utils as vocab_utils
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
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = pat.Parser(corpus_store)
        parser.parse(self.html)

        expected = [
            ['test', 'ヘッダー1'],
            ['ヘッダー1', 'こんにちは。'],
            ['こんにちは。', 'さようなら。'],
        ]
        self.assertListEqual(expected, corpus_store.data)

        expected = ['test', 'ヘッダー', '1', 'こんにちは', '。', 'さようなら']
        self.assertListEqual(expected, vocab.words_new)

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
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = pah.Parser(corpus_store)
        parser.parse(self.htmlStruct)

        expected = [
            ['H4-A', 'body H4-A-1'],
            ['H1-A', 'body H1-A-1'],
            ['H1-A', 'H3-A'],
            ['H1-A', 'H2-A'],
            ['H3-A', 'body H3-A-1'],
            ['H2-A', 'body H2-A-1'],
            ['H1-B', 'body H1-B-1']
        ]
        self.assertListEqual(expected, corpus_store.data)

    def test_AtomicHeaderBodyParserJpn(self):
        """Test the targetted atomic parser with Japanese sentence."""
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = pah.Parser(corpus_store)
        html = ('<html><head><title>test</title></head>'
            '<body>'
            '<h1>ヘッダー1</h1>'
            '<p>こんにちは。さようなら。</p>'
            '</body></html>')
        parser.parse(html)

        expected = [
            ['ヘッダー1','こんにちは。'],
            ['ヘッダー1','さようなら。']
        ]
        self.assertListEqual(expected, corpus_store.data)

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
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = phb.Parser(corpus_store, 'h1')
        parser.parse(self.htmlStruct)

        expected = [
            ['H1-A', 'body H1-A-1\nbody H2-A-1\nbody H2-B-1\nbody H2-B-2\nbody H3-A-1\nbody H2-C-1'],
            ['H1-B', 'body H3-A-1\nbody H2-A-1']
        ]
        self.assertListEqual(expected, corpus_store.data)

    def test_parse_h2(self):
        """Test H2"""
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = phb.Parser(corpus_store, 'h2')
        parser.parse(self.htmlStruct)

        expected = [
            ['H2-A', 'body H2-A-1'],
            ['H2-B', 'body H2-B-1\nbody H2-B-2\nbody H3-A-1'],
            ['H2-C', 'body H2-C-1'],
            ['H2-A', 'body H2-A-1']
        ]
        self.assertListEqual(expected, corpus_store.data)

    def test_parse_h3(self):
        """Test H3"""
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = phb.Parser(corpus_store, 'h3')
        parser.parse(self.htmlStruct)

        expected = [
            ['H3-A', 'body H3-A-1'],
            ['H3-A', 'body H3-A-1']
        ]
        self.assertListEqual(expected, corpus_store.data)

    def test_parse_script(self):
        """Test script element within a font element"""
        vocab = vocab_utils.VocabStore()
        corpus_store = corpus_utils.CorpusStore(vocab)
        parser = phb.Parser(corpus_store)

        html = ('<html><head><title>test</title></head>'
            '<body>'
            '<h1>H1-A</h1>'
            '<font>font element body'
            '<script>script shouldn\'t be parsed</script>'
            '</font>'
            '</body></html>')

        parser.parse(html)

        expected = [
            ['H1-A', 'font element body'],
        ]
        self.assertListEqual(expected, corpus_store.data)


if __name__ == "__main__":
    unittest.main()

