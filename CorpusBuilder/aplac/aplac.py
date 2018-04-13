# -*- coding: utf-8 -*-

import resources.loader as rl

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

