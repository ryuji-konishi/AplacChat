import sys
sys.path.insert(0, '..\\')  # This is required to import common

import unittest
import utils.DataStore as ds
import utils.utils as utils

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


