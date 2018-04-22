# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '..\\')  # This is required to import common
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
            self.tagger.tag('Apple'),
            [u'<c1>', u'apple'])
        self.assertListEqual(
            self.tagger.tag('APPLE'),
            [u'<c2>', u'apple'])
        self.assertListEqual(
            self.tagger.tag('apple'),
            [u'apple'])
        self.assertListEqual(
            self.tagger.tag('aPple'),
            [u'aPple'])
        
    def test_untag(self):
        self.assertEqual(
            self.tagger.untag([u'<c1>', u'apple']),
            'Apple')
        self.assertEqual(
            self.tagger.untag([u'<c2>', u'apple']),
            'APPLE')
        self.assertEqual(
            self.tagger.untag([u'apple']),
            'apple')
        self.assertEqual(
            self.tagger.untag([u'aPple']),
            'aPple')
        


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
            self.tokenizer.split(u"abc高い山def"), 
            [u'abc', u'高い', u'山', u'def'])
        self.assertListEqual(
            self.tokenizer.split(u"abc def高い　山"), 
            [u'abc', u'def', u'高い', u'<fp>', u'山'])
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
            self.tokenizer.split(u"\"abc\""), 
            [u'"', u'abc', u'"'])

    def test_concatenate(self):
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'def']) == 
            "abc def")
        self.assertTrue(
            self.tokenizer.concatenate([u'<c1>', u'that', u"isn't", u'cat', u'.', u'<c1>', u'that', u'is', u'a', u'dog', u'.']) ==
            "That isn't cat. That is a dog.")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'高い', u'山', u'def']) ==
            "abc高い山def")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'def', u'高い', u'<fp>', u'山']) ==
            "abc def高い　山")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'<br>', u'def']) ==
            "abc\ndef")
        self.assertTrue(
            self.tokenizer.concatenate([u'abc', u'<sp>', u'def']) ==
            "abc  def")

if __name__ == "__main__":
    unittest.main()

