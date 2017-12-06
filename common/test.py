# -*- coding: utf-8 -*-
import sys

print sys.getdefaultencoding()
print sys.stdout.encoding

a = 'あ'.decode()
a = unicode('あ')
a = '\xe3\x81\x82'.decode()

a = 'あ'.decode('utf-8')
a = unicode('あ', 'utf-8')
a = '\xe3\x81\x82'.decode('utf-8')


def test(word):
    buf = ''
    for char in word:
        c = ord(char)
        if c < 128:
            print str(c)
        else:
            print str(c)

def mydec(text):
    d = text.decode('utf-8')
    print "{0} decodes {1}".format(text, repr(d))

mydec('あ')                   # \xe3\x81\x82


test('あ')                   # \xe3\x81\x82
test('あ'.decode('utf-8'))   # u3042
test('あ'.decode('utf-8').encode('utf-16'))   # u3042

