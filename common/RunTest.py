# -*- coding: utf-8 -*-
import vocab
import unittest

class TestVocabUtils(unittest.TestCase):
    def setUp(self):
        pass

    def test_delimit_multi_char_text(self):
        self.assertListEqual(
            vocab.delimit_multi_char_text("abc def"), 
            ['abc', 'def'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("abc,def"), 
            ['abc', ',', 'def'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("01234 56789"), 
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("That isn't cat. That is a dog."), 
            ['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("abcあいうdef"), 
            ['abc', 'あ', 'い', 'う', 'def'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("abc defあい　うえお"), 
            ['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("abc\ndef"), 
            ['abc', '<br>', 'def'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("abc  def"), 
            ['abc', '<sp>', 'def'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("(abc def)"), 
            ['(', 'abc', 'def', ')'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("()"),            # empty in brackets
            ['(', ')'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("(abc def."),     # close bracket is missing
            ['(abc', 'def', '.'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("abc def)."),     # open bracket is missing
            ['abc', 'def)', '.'])
        self.assertListEqual(
            vocab.delimit_multi_char_text(")("),            # wrong order
            [')('])
        self.assertListEqual(
            vocab.delimit_multi_char_text(")(abc)"),
            [')', '(', 'abc', ')'])
        self.assertListEqual(
            vocab.delimit_multi_char_text("\"abc\""), 
            ['"', 'abc', '"'])

    def test_concatenate_multi_char_list(self):
        self.assertTrue(
            vocab.concatenate_multi_char_list(['abc', 'def']) == 
            "abc def")
        self.assertTrue(
            vocab.concatenate_multi_char_list(['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.']) ==
            "That isn't cat. That is a dog.")
        self.assertTrue(
            vocab.concatenate_multi_char_list(['abc', 'あ', 'い', 'う', 'def']) ==
            "abcあいうdef")
        self.assertTrue(
            vocab.concatenate_multi_char_list(['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お']) ==
            "abc defあい　うえお")
        self.assertTrue(
            vocab.concatenate_multi_char_list(['abc', '<br>', 'def']) ==
            "abc\ndef")
        self.assertTrue(
            vocab.concatenate_multi_char_list(['abc', '<sp>', 'def']) ==
            "abc  def")

if __name__ == "__main__":
    unittest.main()

