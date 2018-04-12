# -*- coding: utf-8 -*-
import json
import os, sys
import csv

class _ResourceLoader(object):
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

class _SingleColInitLoader(_ResourceLoader):
    """ Single column, initializable resource loader.
        The table has one column. If the text starts from '#', the row is ignored.
        The initial data is loaded from CSV file during development.
        The updated data is stored into JSON file.
    """
    def __init__(self, folder_name, file_json, file_csv):
        _ResourceLoader.__init__(self, folder_name)
        self.file_json = file_json
        self.file_csv = file_csv
        # Check if json file exists. If not, generate csv file from it.
        # This is to run only once in the development phase.
        json_path = self._get_file_path(self.file_json)
        if not os.path.isfile(json_path):
            data = []
            csv_data = self.load_csv(self.file_csv)
            for row in csv_data:
                c = row[0]
                if c[0] == '#':     # if the line starts from '#', comment out.
                    continue
                data.append(c)
            self.save_json(self.file_json, data)

    def load(self):
        return self.load_json(self.file_json)

    def refresh(self):
        data = self.load_json(self.file_json)
        data = self.remove_duplicate(data)
        self.save_json(self.file_json, data)

class _TwoColInitLoader(_ResourceLoader):
    """ Two columns, initializable resource loader.
        The table has two columns.
        The initial data is loaded from CSV file during development.
        The updated data is stored into JSON file.
    """
    def __init__(self, folder_name, file_json, file_csv):
        _ResourceLoader.__init__(self, folder_name)
        self.file_json = file_json
        self.file_csv = file_csv
        # Check if json file exists. If not, generate csv file from it.
        # This is to run only once in the development phase.
        json_path = self._get_file_path(self.file_json)
        if not os.path.isfile(json_path):
            data = []
            csv_data = self.load_csv(self.file_csv)
            for row in csv_data:
                data.append([row[0], row[1]])
            self.save_json(self.file_json, data)

    def load(self):
        return self.load_json(self.file_json)

    def refresh(self):
        data = self.load_json(self.file_json)
        data = self.remove_duplicate(data)
        self.save_json(self.file_json, data)

class _MultiColInitLoader(_ResourceLoader):
    """ Multi columns, initializable resource loader.
        The table has multiple columns. The first col is src, the following cols are tgts.
        The initial data is loaded from CSV file during development.
        The updated data is stored into JSON file.
    """
    def __init__(self, folder_name, file_json, file_csv):
        _ResourceLoader.__init__(self, folder_name)
        self.file_json = file_json
        self.file_csv = file_csv
        # Check if json file exists. If not, generate csv file from it.
        # This is to run only once in the development phase.
        json_path = self._get_file_path(self.file_json)
        if not os.path.isfile(json_path):
            data = []
            csv_data = self.load_csv(self.file_csv)
            for row in csv_data:
                for i in range(1,len(row)):
                    data.append([row[0], row[i]])
            self.save_json(self.file_json, data)

    def load(self):
        return self.load_json(self.file_json)

    def refresh(self):
        data = self.load_json(self.file_json)
        data = self.remove_duplicate(data)
        self.save_json(self.file_json, data)

class NameLoader(_ResourceLoader):
    """ Name resource loader class.
    """
    def __init__(self):
        _ResourceLoader.__init__(self, "name")
        self.file_json = "names_jpn.json"

    def load_names(self):
        """ Load and return a table sum of lastname and firstname. """
        data = self.load_json(self.file_json)
        lastnames = data['lastname']
        firstnames = data['firstname']
        lastnames.extend(firstnames)
        return lastnames

    def refresh(self):
        data = self.load_json(self.file_json)
        lastnames = data['lastname']
        data['lastname'] = self.remove_duplicate(lastnames)
        firstnames = data['firstname']
        data['firstname'] = self.remove_duplicate(firstnames)
        self.save_json(self.file_json, data)

class CountryLoader(_ResourceLoader):
    """ Country resource loader class.
    """
    def __init__(self):
        _ResourceLoader.__init__(self, "country")
        self.file_json = "country.json"

    def load_countries(self):
        """ Load and return a table sum of country names in both English and Japanese. """
        data = self.load_json(self.file_json)
        result = data['eng']
        result.extend(data['jpn'])
        return result

    def refresh(self):
        data = self.load_json(self.file_json)
        eng = data['eng']
        data['eng'] = self.remove_duplicate(eng)
        jpn = data['jpn']
        data['jpn'] = self.remove_duplicate(jpn)
        self.save_json(self.file_json, data)

class SaluteLoader(object):
    """ Salute resource loader class.
        The initial data is loaded from CSV file during development.
    """
    def __init__(self):
        self.delegate = _MultiColInitLoader('salute', 'salute.json', 'salute.csv')

    def load_salutes(self):
        """ Load and return a set of source/target list. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class ConversationLoader(object):
    """ Conversation resource loader class.
        The initial data is loaded from CSV file during development.
    """
    def __init__(self):
        self.delegate = _MultiColInitLoader('conversation', 'conversation.json', 'conversation.csv')

    def load_conversations(self):
        """ Load and return a set of source/target list. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class JoyoKanjiLoader(object):
    """ Joyo-kanji resource loader class.
    """
    def __init__(self):
        self.delegate = _SingleColInitLoader('kanji_joyo', 'joyo_kanji_code.json', 'joyo-kanji-code-u.csv')

    def load_kanjis(self):
        """ Load and return a list of Joyo-Kanji charactors. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class JinmeiKanjiLoader(object):
    """ Jinmeiyou-kanji resource loader class.
    """
    def __init__(self):
        self.delegate = _SingleColInitLoader('kanji_jinmeiyo', 'jinmei_kanji_code.json', 'jinmeiyou-kanji-code-u.csv')

    def load_kanjis(self):
        """ Load and return a list of Joyo-Kanji charactors. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class CityLoader(object):
    """ City name resource loader class.
    """
    def __init__(self):
        self.delegate = _SingleColInitLoader('city', 'city.json', None)

    def load_cities(self):
        """ Load and return a list of city names """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()
