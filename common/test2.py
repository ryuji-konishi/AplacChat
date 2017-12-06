# -*- coding: utf-8 -*-

def test(word):
    buf = ''
    for char in word:
        c = ord(char)
        if c < 128:
            print str(c)
        else:
            print str(c)


test('あ')

