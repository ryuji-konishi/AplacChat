import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os, errno
import filecmp
import unittest
import utils.corpus_utils as corpus_utils
import utils.utils as utils
import utils.vocab_utils as vocab_utils
from common import tokenizer as tk

special_tokens = tk.special_tokens

class TestVocabStore(unittest.TestCase):
    def setUp(self):
        self.filename1 = 'tmp1'
        self.filename2 = 'tmp2'
        self._silentremove(self.filename1)
        self._silentremove(self.filename2)
        
    def tearDown(self):
        self._silentremove(self.filename1)
        self._silentremove(self.filename2)

    def test_CreateNewFile(self):
        vocab = vocab_utils.VocabStore(self.filename1)
        vocab.add_vocab_words(['abc', 'abc', 'def'])
        vocab.save_to_file()

        with open(self.filename2, 'w', encoding='utf8') as the_file:
            self._write_special_tokens(the_file)
            the_file.write('abc\n')
            the_file.write('def\n')
        self.assertTrue(filecmp.cmp(self.filename1, self.filename2))

    def test_LoadExistingFile(self):
        # Create original file before VocabStore
        with open(self.filename1, 'w', encoding='utf8') as the_file:
            self._write_special_tokens(the_file)
            the_file.write('abc\n')
            the_file.write('def\n')
        
        vocab = vocab_utils.VocabStore(self.filename1)
        vocab.add_vocab_words(['abc', '123'])
        vocab.save_to_file()

        with open(self.filename2, 'w', encoding='utf8') as the_file:
            self._write_special_tokens(the_file)
            the_file.write('abc\n')
            the_file.write('def\n')
            the_file.write('123\n')
        
        self.assertTrue(filecmp.cmp(self.filename1, self.filename2))

    def test_print_report(self):
        vocab = vocab_utils.VocabStore(self.filename1)
        vocab.add_vocab_words(['abc', 'abc', 'def'])
        vocab.save_to_file()

        def myprint(*arg):
            a = [str(elem) for elem in arg]
            print(' '.join(a))

        vocab.print_report(myprint)

    def _write_special_tokens(self, the_file):
        for t in special_tokens:
            the_file.write(t + '\n')

    def _silentremove(self, filename):
        try:
            os.remove(filename)
        except OSError as e: # this would be "except OSError, e:" before Python 2.6
            if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
                raise # re-raise exception if a different error occurred

class TestCorpusStore(unittest.TestCase):
    def setUp(self):
        pass

    def test_store_data(self):
        corpus_store = corpus_utils.CorpusStore()

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
        corpus_store = corpus_utils.CorpusStore()

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

    def test_validation(self):
        """ Test if validation works. Validator checks src and tgt texts, and only if
            they are valid, the texts are stored.
        """
        def validator(source, target):
            if 'boom' in source or 'boom' in target:
                return '', ''
            else:
                return source, target

        corpus_store = corpus_utils.CorpusStore(func_validate = validator)

        corpus_store.store_data('source text', 'target text')
        corpus_store.store_data('boom', 'target text')
        corpus_store.store_data('source text', 'boom')
        self.assertTrue(
            corpus_store.data, 
            ['source text', 'target text'])
        corpus_store.clear()


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_sort_unicode_word_list(self):
        words = ['c', 'b', 'a']
        expected = ['a', 'b', 'c']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

        words = ['ac', 'ab', 'aa']
        expected = ['aa', 'ab', 'ac']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

        words = [u'う', u'い', u'あ']
        expected = [u'あ', u'い', u'う']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

        words = [u'あう', u'あい', u'ああ']
        expected = [u'ああ', u'あい', u'あう']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

        words = [u'ああ', u'あ']
        expected = [u'あ', u'ああ']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

        words = [u'あa', u'あA']
        expected = [u'あA', u'あa']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

        # make sure it really sorts by Unicode code point across 0x00** - 0x30**
        words = [u'ゑ', u'め', u'ぱ', u'ち', u'け', u'ぁ', u'〱', u'〡', u'】', u'、', u'q', u'a', u'Q', u'A', u'1', u'!']
        expected = [u'!', u'1', u'A', u'Q', u'a', u'q', u'、', u'】', u'〡', u'〱', u'ぁ', u'け', u'ち', u'ぱ', u'め', u'ゑ']
        utils.sort_unicode_word_list(words)
        self.assertListEqual(expected, words)

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
        actual1, actual2 = utils.distribute(lst, ratio)
        self.assertListEqual(['a', 'b'], actual1)
        self.assertListEqual(['c', 'd'], actual2)

        ratio = (0.5, 0.25, 0.25)
        actual1, actual2, actual3 = utils.distribute(lst, ratio)
        self.assertListEqual(['a', 'b'], actual1)
        self.assertListEqual(['c'], actual2)
        self.assertListEqual(['d'], actual3)

        lst = [i for i in range(10)]

        ratio = (0.5, 0.2, 0.3)
        actual1, actual2, actual3 = utils.distribute(lst, ratio)
        self.assertListEqual([0, 1, 2, 3, 4], actual1)
        self.assertListEqual([5, 6], actual2)
        self.assertListEqual([7, 8, 9], actual3)

if __name__ == "__main__":
    unittest.main()


