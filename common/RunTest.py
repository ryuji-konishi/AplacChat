# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '..\\')  # This is required to import common
# If importing common doesn't go well, check the Python interpreter's current working directory.
# This has to be 'common' folder.
# import os
# print(os.getcwd())  # print current working directory


import unittest
from common import SentenseResolver as sr

class TestLetterCaseTagger(unittest.TestCase):
    def setUp(self):
        self.tagger = sr.LetterCaseTagger()

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
        self.resolver = sr.SentenseResolver()

    def test_split(self):
        self.assertListEqual(
            self.resolver.split(u"abc def"), 
            [u'abc', u'def'])
        self.assertListEqual(
            self.resolver.split(u"abc,def"), 
            [u'abc', u',', u'def'])
        self.assertListEqual(
            self.resolver.split(u"01234 56789"), 
            [u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9'])
        self.assertListEqual(
            self.resolver.split(u"That isn't cat. That is a dog."), 
            [u'<c1>', u'that', "isn't", 'cat', u'.', u'<c1>', u'that', u'is', u'a', u'dog', u'.'])
        self.assertListEqual(
            self.resolver.split(u"abcあいうdef"), 
            [u'abc', u'あ', u'い', u'う', u'def'])
        self.assertListEqual(
            self.resolver.split(u"abc defあい　うえお"), 
            [u'abc', u'def', u'あ', u'い', u'　', u'う', u'え', u'お'])
        self.assertListEqual(
            self.resolver.split(u"abc\ndef"), 
            [u'abc', u'<br>', u'def'])
        self.assertListEqual(
            self.resolver.split(u"abc  def"), 
            [u'abc', u'<sp>', u'def'])
        self.assertListEqual(
            self.resolver.split(u"(abc def)"), 
            [u'(', u'abc', u'def', u')'])
        self.assertListEqual(
            self.resolver.split(u"()"),            # empty in brackets
            [u'(', u')'])
        self.assertListEqual(
            self.resolver.split(u"(abc def."),     # close bracket is missing
            [u'(', u'abc', u'def', u'.'])
        self.assertListEqual(
            self.resolver.split(u"abc def)."),     # open bracket is missing
            [u'abc', u'def', u')', u'.'])
        self.assertListEqual(
            self.resolver.split(u")("),            # wrong order
            [u')', u'('])
        self.assertListEqual(
            self.resolver.split(u")(abc)"),
            [u')', u'(', u'abc', u')'])
        self.assertListEqual(
            self.resolver.split(u"\"abc\""), 
            [u'"', u'abc', u'"'])

    def test_concatenate(self):
        self.assertTrue(
            self.resolver.concatenate([u'abc', u'def']) == 
            "abc def")
        self.assertTrue(
            self.resolver.concatenate([u'<c1>', u'that', "isn't", 'cat', u'.', u'<c1>', u'that', u'is', u'a', u'dog', u'.']) ==
            "That isn't cat. That is a dog.")
        self.assertTrue(
            self.resolver.concatenate([u'abc', u'あ', u'い', u'う', u'def']) ==
            "abcあいうdef")
        self.assertTrue(
            self.resolver.concatenate([u'abc', u'def', u'あ', u'い', u'　', u'う', u'え', u'お']) ==
            "abc defあい　うえお")
        self.assertTrue(
            self.resolver.concatenate([u'abc', u'<br>', u'def']) ==
            "abc\ndef")
        self.assertTrue(
            self.resolver.concatenate([u'abc', u'<sp>', u'def']) ==
            "abc  def")

if __name__ == "__main__":
    unittest.main()

