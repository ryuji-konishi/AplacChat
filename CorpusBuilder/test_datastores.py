import sys
sys.path.insert(0, '..\\')  # This is required to import common

import os, errno
import filecmp
import unittest
import utils.DataStore as ds
from common import SentenseResolver as sr

special_tokens = sr.special_tokens

class TestVocabStore(unittest.TestCase):
    def setUp(self):
        self.filename1 = 'tmp1'
        self.filename2 = 'tmp2'
        silentremove(self.filename1)
        silentremove(self.filename2)
        
    def tearDown(self):
        silentremove(self.filename1)
        silentremove(self.filename2)

    def test_CreateNewFile(self):
        vocab = ds.VocabStore(self.filename1)
        vocab.add_vocab_words(['abc', 'abc', 'def'])
        vocab.save_to_file()

        with open(self.filename2, 'w', encoding='utf8') as the_file:
            write_special_tokens(the_file)
            the_file.write('abc\n')
            the_file.write('def\n')
        self.assertTrue(filecmp.cmp(self.filename1, self.filename2))

    def test_LoadExistingFile(self):
        # Create original file before VocabStore
        with open(self.filename1, 'w', encoding='utf8') as the_file:
            write_special_tokens(the_file)
            the_file.write('abc\n')
            the_file.write('def\n')
        
        vocab = ds.VocabStore(self.filename1)
        vocab.add_vocab_words(['abc', '123'])
        vocab.save_to_file()

        with open(self.filename2, 'w', encoding='utf8') as the_file:
            write_special_tokens(the_file)
            the_file.write('abc\n')
            the_file.write('def\n')
            the_file.write('123\n')
        
        self.assertTrue(filecmp.cmp(self.filename1, self.filename2))

def write_special_tokens(the_file):
    for t in special_tokens:
        the_file.write(t + '\n')

def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred

if __name__ == "__main__":
    unittest.main()

