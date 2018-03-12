import json
import os, sys

class Dictionary(object):
    ENG = "english"
    def __init__(self, lang = ENG):
        if lang.lower() == self.ENG:
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
    def __init__(self):
        self.words_map = None
        # Load dictionary file
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            filename = current_dir + "\\English\\words_dictionary.json"
            with open(filename, "r") as english_dictionary:
                self.words_map = json.load(english_dictionary)
        except Exception as e:
            return str(e)

    def Check(self, word):
        word = word.lower()
        # All the words are assigned with 1 in the dictionary.
        return self.words_map[word] == 1
