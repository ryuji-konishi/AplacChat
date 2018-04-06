# -*- coding: utf-8 -*-
import json
import os, sys


class Loader(object):
    def __init__(self, folder_name, file_name):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.folder = folder_name
        self.file = file_name

    def load_data(self):
        filepath = os.path.join(self.current_dir, self.folder, self.file)
        with open(filepath, "r", encoding='utf8') as fp:
            data = json.load(fp)
        return data

    def save_data(self, data):
        filepath = os.path.join(self.current_dir, self.folder, self.file)
        with open(filepath, 'w', encoding='utf8') as fp:
            json.dump(data, fp, ensure_ascii=False)

    def remove_duplicate(self, lst):
        """ Remove duplicates from the given list. """
        return list(set(lst))

class NameLoader(Loader):
    """ Name resource loader class.
    """
    def __init__(self):
        Loader.__init__(self, "name", "names_jpn.json")

    def load_names(self):
        """ Load and return a table of lastname and firstname. """
        data = self.load_data()
        return data['lastname'], data['firstname']

    def refresh(self):
        data = self.load_data()
        lastnames = data['lastname']
        data['lastname'] = self.remove_duplicate(lastnames)
        firstnames = data['firstname']
        data['firstname'] = self.remove_duplicate(firstnames)
        self.save_data(data)


