import sys
sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import utils.DataStore as ds
import utils.utils as utils

class TestCorpusStore(unittest.TestCase):
    def setUp(self):
        pass

    def test_store_data(self):
        corpus_store = ds.CorpusStore()

        # If the input to the corpus store is either
        # - a line of text or
        # - a list of text
        # the result will be the same shaped list of text.
        corpus_store.store_data('source text', 'target text')
        self.assertTrue(
            corpus_store.data, 
            ['source text', 'target text'])
        corpus_store.clear()

        corpus_store.store_data(['source text'], ['target text'])
        self.assertTrue(
            corpus_store.data, 
            ['source text', 'target text'])
        corpus_store.clear()

        # The result is broken into multiple lines if multiple inputs are stored.
        corpus_store.store_data(['source text1', 'source text2'], ['target text1', 'target text2'])
        self.assertTrue(
            corpus_store.data, 
            [['source text1', 'target text1'],
            ['source text2', 'target text2']])
        corpus_store.clear()

        # The result is broken into words space ' ' separated.
        # If the input text is multi-byte character, each character is separated.
        corpus_store.store_data(['source text', 'ソース'], ['target text', 'ターゲット'])
        self.assertTrue(
            corpus_store.data, 
            [['source text', 'target text'],
            ['ソ ー ス', 'ターゲット']])
        corpus_store.clear()

        # The input is single line of source and multi lines of target.
        corpus_store.store_data('source line', 'target line1\ntarget line2')
        self.assertTrue(
            corpus_store.data, 
            ['source line', 'target line <br> target line2'])
        corpus_store.clear()

    def test_split(self):
        corpus_store = ds.CorpusStore()

        corpus_store.store_data(
            ['source a', 'source b', 'source c', 'source d'], 
            ['target a', 'target b', 'target c', 'target d'])

        ratio = (0.5, 0.5)
        actual = corpus_store.split(ratio)
        self.assertEqual(len(actual), 2)
        expected = [
            ['source a', 'target a'],
            ['source b', 'target b']
            ]
        self.assertListEqual(expected, actual[0].data)
        expected = [
            ['source c', 'target c'],
            ['source d', 'target d']
            ]
        self.assertListEqual(expected, actual[1].data)

        ratio = (0.5, 0.25, 0.25)
        actual = corpus_store.split(ratio)
        self.assertEqual(len(actual), 3)
        expected = [
            ['source a', 'target a'],
            ['source b', 'target b']
            ]
        self.assertListEqual(expected, actual[0].data)
        expected = [
            ['source c', 'target c']
            ]
        self.assertListEqual(expected, actual[1].data)
        expected = [
            ['source d', 'target d']
            ]
        self.assertListEqual(expected, actual[2].data)

        corpus_store.clear()


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


