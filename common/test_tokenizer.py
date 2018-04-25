# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '..//')  # This is required to import common
# If importing common doesn't go well, check the Python interpreter's current working directory.
# This has to be 'common' folder.
# import os
# print(os.getcwd())  # print current working directory


import unittest
from common import tokenizer as tk

class TestLetterCaseTagger(unittest.TestCase):
    def setUp(self):
        self.tagger = tk.LetterCaseTagger()

    def test_tag(self):
        self.assertListEqual(
            self.tagger.tag(u'Apple'),
            [u'<c1>', u'apple'])
        self.assertListEqual(
            self.tagger.tag(u'APPLE'),
            [u'<c2>', u'apple'])
        self.assertListEqual(
            self.tagger.tag(u'apple'),
            [u'apple'])
        self.assertListEqual(
            self.tagger.tag(u'aPple'),
            [u'aPple'])
        
    def test_untag(self):
        self.assertEqual(
            self.tagger.untag([u'<c1>', u'apple']),
            u'Apple')
        self.assertEqual(
            self.tagger.untag([u'<c2>', u'apple']),
            u'APPLE')
        self.assertEqual(
            self.tagger.untag([u'apple']),
            u'apple')
        self.assertEqual(
            self.tagger.untag([u'aPple']),
            u'aPple')
        


class TestSentenseResulver(unittest.TestCase):
    def setUp(self):
        self.tokenizer = tk.tokenizer()

    def test_split(self):
        self.assertListEqual(
            self.tokenizer.split(u"abc def"), 
            [u'abc', u'def'])
        self.assertListEqual(
            self.tokenizer.split(u"abc,def"), 
            [u'abc', u',', u'def'])
        self.assertListEqual(
            self.tokenizer.split(u"01234 56789"), 
            [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9'])
        self.assertListEqual(
            self.tokenizer.split(u"１２３４５６７８９８０"), 
            [u'１', u'２', u'３', u'４', u'５', u'６', u'７', u'８', u'９', u'８', u'０'])
        self.assertListEqual(
            self.tokenizer.split(u"~!@#$%^&*()_+=[];',./{}:\"<>?"), 
            [u'~', u'!', u'@', u'#', u'$', u'%', u'^', u'&', u'*', u'(', u')', u'_', u'+', 
            u'=', u'[', u']', u';', u"'", u',', u'.', u'/', u'{', u'}', u':', u'"', u'<', u'>', u'?'])
        self.assertListEqual(
            self.tokenizer.split(u"‘～！＠＃＄％＾＆＊（）＿＋－＝「」；’、。・｛｝：”＜＞？"), 
            [u'‘', u'～', u'！', u'＠', u'＃', u'＄', u'％', u'＾', u'＆', u'＊', u'（', u'）', u'＿', u'＋', 
            u'－', u'＝', u'「', u'」', u'；', u'’', u'、', u'。', u'・', u'｛', u'｝', u'：', u'”', u'＜', u'＞', u'？'])
        self.assertListEqual(
            self.tokenizer.split(u"That isn't cat. That is a dog."), 
            [u'<c1>', u'that', u"isn't", u'cat', u'.', u'<c1>', u'that', u'is', u'a', u'dog', u'.'])
        self.assertListEqual(
            self.tokenizer.split(u"abcあいうdef"),
            [u'abc', u'あ', u'い', u'う', u'def'])
        self.assertListEqual(
            self.tokenizer.split(u"abc defあい　うえお"),
            [u'abc', u'def', u'あ', u'い', u'<fp>', u'う', u'え', u'お'])
        self.assertListEqual(
            self.tokenizer.split(u"abc\ndef"), 
            [u'abc', u'<br>', u'def'])
        self.assertListEqual(
            self.tokenizer.split(u"abc  def"), 
            [u'abc', u'<sp>', u'def'])
        self.assertListEqual(
            self.tokenizer.split(u"(abc def)"), 
            [u'(', u'abc', u'def', u')'])
        self.assertListEqual(
            self.tokenizer.split(u"He said \"What's up?\""), 
            [u'<c1>', u'he', u'said', u'"', u'<c1>', u"what's", u'up', u'?', u'"'])

    def test_concatenate(self):
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'def']) == 
            u"abc def")
        self.assertTrue(
            self.tokenizer.concatenate([u'<c1>', u'that', u"isn't", u'cat', u'.', u'<c1>', u'that', u'is', u'a', u'dog', u'.']) ==
            u"That isn't cat. That is a dog.")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'あ', u'い', u'う', u'def']) ==
            "abcあいうdef")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'def', u'あ', u'い', u'<fp>', u'う', u'え', u'お']) ==
            "abc defあい　うえお")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'<br>', u'def']) ==
            u"abc\ndef")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'<sp>', u'def']) ==
            u"abc  def")

if __name__ == "__main__":
    unittest.main()

