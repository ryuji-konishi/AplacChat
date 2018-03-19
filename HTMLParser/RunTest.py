import sys
sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import ParserAtomic as pat
import ParserAtomicHeaderBody as pah
import ParserHeaderBody as phb
import DataStore as ds
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

    def test_distribute(self):
        lst = ['a', 'b', 'c', 'd']

        ratio = (0.5, 0.5)
        actual = utils.distribute(lst, ratio)
        expected = [
            ['a', 'b'],
            ['c', 'd']
            ]
        self.assertCountEqual(expected, actual)

        ratio = (0.5, 0.25, 0.25)
        actual = utils.distribute(lst, ratio)
        expected = [
            ['a', 'b'],
            ['c'],
            ['d']
            ]
        self.assertCountEqual(expected, actual)

        lst = [i for i in range(10)]

        ratio = (0.5, 0.2, 0.3)
        actual = utils.distribute(lst, ratio)
        expected = [
            [0, 1, 2, 3, 4],
            [5, 6],
            [7, 8, 9]
            ]
        self.assertCountEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()

