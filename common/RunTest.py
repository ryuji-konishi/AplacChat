# -*- coding: utf-8 -*-
import vocab
import unittest
import SentenseResolver as sr

class TestSentenseResulver(unittest.TestCase):
    def setUp(self):
        self.r = sr.SentenseResolver()

    def test_delimit_multi_char_text(self):
        self.assertListEqual(
            self.r.split("abc def"), 
            ['abc', 'def'])
        self.assertListEqual(
            self.r.split("abc,def"), 
            ['abc', ',', 'def'])
        self.assertListEqual(
            self.r.split("01234 56789"), 
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.assertListEqual(
            self.r.split("That isn't cat. That is a dog."), 
            ['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.'])
        self.assertListEqual(
            self.r.split("abcあいうdef"), 
            ['abc', 'あ', 'い', 'う', 'def'])
        self.assertListEqual(
            self.r.split("abc defあい　うえお"), 
            ['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お'])
        self.assertListEqual(
            self.r.split("abc\ndef"), 
            ['abc', '<br>', 'def'])
        self.assertListEqual(
            self.r.split("abc  def"), 
            ['abc', '<sp>', 'def'])
        self.assertListEqual(
            self.r.split("(abc def)"), 
            ['(', 'abc', 'def', ')'])
        self.assertListEqual(
            self.r.split("()"),            # empty in brackets
            ['(', ')'])
        self.assertListEqual(
            self.r.split("(abc def."),     # close bracket is missing
            ['(abc', 'def', '.'])
        self.assertListEqual(
            self.r.split("abc def)."),     # open bracket is missing
            ['abc', 'def)', '.'])
        self.assertListEqual(
            self.r.split(")("),            # wrong order
            [')('])
        self.assertListEqual(
            self.r.split(")(abc)"),
            [')', '(', 'abc', ')'])
        self.assertListEqual(
            self.r.split("\"abc\""), 
            ['"', 'abc', '"'])

    def test_concatenate_multi_char_list(self):
        self.assertTrue(
            self.r.concatenate(['abc', 'def']) == 
            "abc def")
        self.assertTrue(
            self.r.concatenate(['That', "isn't", 'cat', '.', 'That', 'is', 'a', 'dog', '.']) ==
            "That isn't cat. That is a dog.")
        self.assertTrue(
            self.r.concatenate(['abc', 'あ', 'い', 'う', 'def']) ==
            "abcあいうdef")
        self.assertTrue(
            self.r.concatenate(['abc', 'def', 'あ', 'い', '　', 'う', 'え', 'お']) ==
            "abc defあい　うえお")
        self.assertTrue(
            self.r.concatenate(['abc', '<br>', 'def']) ==
            "abc\ndef")
        self.assertTrue(
            self.r.concatenate(['abc', '<sp>', 'def']) ==
            "abc  def")

class TestVocabUtils(unittest.TestCase):
    def setUp(self):
        pass

if __name__ == "__main__":
    unittest.main()

