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

    def get_data(self):
        return self.delegate.get_data()

class English(object):
    """ English dictionary class. The dictionary data is originated from https://github.com/dwyl/english-words.git
    """
    # Additional words that don't exist in the original dictionary.
    addons = [u"isn't", u"wasn't", u"aren't", u"weren't", u"don't", u"didn't", u"hasn't", u"haven't", u"hadn't"
        u"ain't", u"it's", u"i'm", u"he's", u"she's", u"they're", u"we're", u"there're",
        u"i've", u"you've", u"we've", u"what's", u"who's", u"where's", u"there's", u"here's"]

    def __init__(self):
        # Load dictionary file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.filename = os.path.join(current_dir, "English", "words_dictionary.json")
        self.words = None

    def _lazy_loading(self):
        """ Initialize self.words value by reading file. This is time and memory consuming, so
            do this only when self.words is required for the first time (lazy loading)
        """
        if not self.words:
            self.words = set()
            with open(self.filename, "r") as english_dictionary:
                words_map = json.load(english_dictionary)
            # Load words from map
            for key in words_map:
                self.words.add(key)
            # Add some more
            for word in self.addons:
                self.words.add(word)

    def get_data(self):
        self._lazy_loading()
        return self.words

    def Check(self, word):
        self._lazy_loading()
        
        word = word.lower()
        # All the words are assigned with 1 in the dictionary.
        if word in self.words:
            return True
        else:
            return False
