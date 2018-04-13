# -*- coding: utf-8 -*-

import resources.loader as rl

myname = '田村'
yourname = '田村さん'
html_target_tag = ['h1', 'h2', 'h3', 'h4', 'h5']

def pair_validate(src, tgt):
    """ This is a function that takes source/target text pairs from the corpus resouces
        or HTML parsers, and it decides if the texts are valid and to be processed and stored into corpus.
        If omitted any texts will be stored.
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

