# -*- coding: utf-8 -*-
import json
import os, sys
import csv

class Loader(object):
    def __init__(self, folder_name):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.folder = folder_name

    def _get_file_path(self, file_name):
        return os.path.join(self.current_dir, self.folder, file_name)
        
    def load_json(self, file_name):
        filepath = self._get_file_path(file_name)
        with open(filepath, "r", encoding='utf8') as fp:
            data = json.load(fp)
        return data

    def save_json(self, file_name, data):
        filepath = self._get_file_path(file_name)
        with open(filepath, 'w', encoding='utf8') as fp:
            json.dump(data, fp, ensure_ascii=False)

    def load_csv(self, file_name):
        filepath = self._get_file_path(file_name)
        with open(filepath, "r", encoding='utf8') as fp:
            reader = csv.reader(fp)
            data = list(reader)
        return data

    def remove_duplicate(self, lst):
        """ Remove duplicates from the given list. """
        return list(set(lst))

class NameLoader(Loader):
    """ Name resource loader class.
    """
    def __init__(self):
        Loader.__init__(self, "name")
        self.file_json = "names_jpn.json"

    def load_names(self):
        """ Load and return a table of lastname and firstname. """
        data = self.load_json(self.file_json)
        return data['lastname'], data['firstname']

    def refresh(self):
        data = self.load_json(self.file_json)
        lastnames = data['lastname']
        data['lastname'] = self.remove_duplicate(lastnames)
        firstnames = data['firstname']
        data['firstname'] = self.remove_duplicate(firstnames)
        self.save_json(self.file_json, data)

class KanjiLoader(Loader):
    """ Joyo-kanji resource loader class.
    """
    def __init__(self, folder_name, file_json, file_csv):
        Loader.__init__(self, folder_name)
        self.file_json = file_json
        self.file_csv = file_csv
        # Check if json file exists. If not, generate csv file from it.
        # This is to run only once in the development phase.
        json_path = self._get_file_path(self.file_json)
        if not os.path.isfile(json_path):
            buf = []
            csv_data = self.load_csv(self.file_csv)
            for row in csv_data:
                c = row[0]
                if c[0] == '#':     # if the line starts from '#', comment out.
                    continue
                buf.append(c)
            self.save_json(self.file_json, buf)

    def load_kanjis(self):
        """ Load and return a list of Joyo-Kanji charactors. """
        data = self.load_json(self.file_json)
        return data

    def refresh(self):
        data = self.load_json(self.file_json)
        data = self.remove_duplicate(data)
        self.save_json(self.file_json, data)

class JoyoKanjiLoader(KanjiLoader):
    """ Joyo-kanji resource loader class.
    """
    def __init__(self):
        KanjiLoader.__init__(self, "kanji_joyo", "joyo_kanji_code.json", "joyo-kanji-code-u.csv")

class JinmeiKanjiLoader(KanjiLoader):
    """ Jinmeiyou-kanji resource loader class.
    """
    def __init__(self):
        KanjiLoader.__init__(self, "kanji_jinmeiyo", "jinmei_kanji_code.json", "jinmeiyou-kanji-code-u.csv")
