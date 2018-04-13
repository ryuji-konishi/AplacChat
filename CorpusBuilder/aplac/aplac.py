# -*- coding: utf-8 -*-

import resources.loader as rl
import utils.vocab_utils as vocab_utils

myname = '田村'
yourname = '田村さん'
html_target_tag = ['h1', 'h2', 'h3', 'h4', 'h5']

def get_symbol_ratio(text):
    """ Calculate the ratio of symbol characters contained in the given text.
        For example, '!@#$%' is 100%, and 'abcdef' is 0%.
    """
    # count the number of symbol characters in text
    cnt = 0
    for char in text:
        if vocab_utils.is_charactor_ascii_symbol(char) or vocab_utils.is_charactor_full_symbol(char):
            cnt += 1

    # return the ratio
    if len(text) == 0:
        return 0
    else:
        return cnt / len(text)

def get_number_ratio(text):
    """ Calculate the ratio of number characters contained in the given text.
        For example, '01234' is 100%, and 'abcdef' is 0%.
    """
    # count the number of number characters in text
    cnt = 0
    for char in text:
        if vocab_utils.is_charactor_ascii_number(char) or vocab_utils.is_charactor_full_number(char):
            cnt += 1

    # return the ratio
    if len(text) == 0:
        return 0
    else:
        return cnt / len(text)

def validate_pair_html(source, target):
    """ This is a function that takes source/target text pairs from the or HTML parsers, 
        and it decides if the texts are valid and to be processed and stored into corpus.
    """
    if get_symbol_ratio(source) >= 0.5:
        print ("source", source, "is skipped")
        return False
    if get_number_ratio(source) >= 0.5:
        print ("source", source, "is skipped")
        return False
    return True

def validate_pair_corpus(source, target):
    """ This is a function that takes source/target text pairs from the corpus resouces,
        and it decides if the texts are valid and to be processed and stored into corpus.
    """
    return True

class SaluteLoader(object):
    """ Salute sentense pair resource loader class.
        The initial data is loaded from CSV file during development.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = rl.MultiColInitLoader(__file__,
            'salute', 'salute_' + lang + '.json', 'salute_' + lang + '.csv')

    def load(self):
        """ Load and return a set of source/target list. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class ConversationLoader(object):
    """ Conversation sentense pair resource loader class.
        The initial data is loaded from CSV file during development.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = rl.MultiColInitLoader(__file__,
            'conversation', 'conversation_' + lang + '.json', 'conversation_' + lang + '.csv')

    def load(self):
        """ Load and return a set of source/target list. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

