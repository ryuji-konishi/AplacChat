# -*- coding: utf-8 -*-
import json
import os, sys

class Dictionary(object):
    ENG = 1
    def __init__(self, lang = ENG):
        if lang == self.ENG:
            self.delegate = English()
        else:
            raise ValueError("Invalid languate type " + lang)

    def Check(self, word):
        """ Check if the assigned word is a valid word and existing in the dictionary, and return True or False. """
        if self.delegate:
            return self.delegate.Check(word)
        else:
            return False

class English(object):
    """ English dictionary class. The dictionary data is originated from https://github.com/dwyl/english-words.git
    """
    # Additional words that don't exist in the original dictionary.
    addons = [u"isn't", u"wasn't", u"aren't", u"weren't", u"don't", u"didn't", u"hasn't", u"haven't", u"hadn't"
        u"ain't", u"it's", u"i'm", u"he's", u"she's", u"they're", u"we're", u"there're"]

    def __init__(self):
        # Load dictionary file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(current_dir, "English", "words_dictionary.json")
        with open(filename, "r") as english_dictionary:
            self.words_map = json.load(english_dictionary)
        # Add some more
        for word in self.addons:
            self.words_map[word] = 1

    def Check(self, word):
        word = word.lower()
        # All the words are assigned with 1 in the dictionary.
        if word in self.words_map:
            return self.words_map[word] == 1
        else:
            return False
