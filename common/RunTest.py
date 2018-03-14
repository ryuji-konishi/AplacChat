# -*- coding: utf-8 -*-
import unittest
import SentenseResolver as sr

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
            [u'That', "isn't", 'cat', u'.', u'That', u'is', u'a', u'dog', u'.'])
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
            [u'(abc', u'def', u'.'])
        self.assertListEqual(
            self.resolver.split(u"abc def)."),     # open bracket is missing
            [u'abc', u'def)', u'.'])
        self.assertListEqual(
            self.resolver.split(u")("),            # wrong order
            [u')('])
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
            self.resolver.concatenate([u'That', "isn't", 'cat', u'.', u'That', u'is', u'a', u'dog', u'.']) ==
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

