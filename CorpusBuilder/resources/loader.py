# -*- coding: utf-8 -*-
import json
import os, sys
import csv

class _ResourceLoader(object):
    def __init__(self, python_file, folder_name):
        """ python_file is the file name of the python code that the child class that inherits this 
            class is defined. This is used to locate the resouce folder path which is supposed to be
            placed within the same path as the python file.
            folder_name is the folder name that the resouce file is contained.
        """
        self.current_dir = os.path.dirname(os.path.realpath(python_file))
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
    def __init__(self, python_file, folder_name, file_json, file_csv):
        """ python_file is the file name of the python code that the child class that inherits this 
            class is defined. This is used to locate the resouce folder path which is supposed to be
            placed within the same path as the python file.
            folder_name is the folder name that the resouce file is contained.
            file_json is the json file that contains the resouce data with data structure.
            file_csv is the csv file that contains the initial data which is converted into json data.
        """
        _ResourceLoader.__init__(self, python_file, folder_name)
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
    def __init__(self, python_file, folder_name, file_json, file_csv):
        """ python_file is the file name of the python code that the child class that inherits this 
            class is defined. This is used to locate the resouce folder path which is supposed to be
            placed within the same path as the python file.
            folder_name is the folder name that the resouce file is contained.
            file_json is the json file that contains the resouce data with data structure.
            file_csv is the csv file that contains the initial data which is converted into json data.
        """
        _ResourceLoader.__init__(self, python_file, folder_name)
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

class MultiColInitLoader(_ResourceLoader):
    """ Multi columns, initializable resource loader.
        The table has multiple columns. The first col is src, the following cols are tgts.
        The initial data is loaded from CSV file during development.
        The updated data is stored into JSON file.
    """
    def __init__(self, python_file, folder_name, file_json, file_csv):
        """ python_file is the file name of the python code that the child class that inherits this 
            class is defined. This is used to locate the resouce folder path which is supposed to be
            placed within the same path as the python file.
            folder_name is the folder name that the resouce file is contained.
            file_json is the json file that contains the resouce data with data structure.
            file_csv is the csv file that contains the initial data which is converted into json data.
        """
        _ResourceLoader.__init__(self, python_file, folder_name)
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

class JoyoKanjiLoader(object):
    """ Joyo-kanji resource loader class.
    """
    def __init__(self):
        self.delegate = _SingleColInitLoader(__file__, 
            'kanji_joyo', 'joyo_kanji_code.json', 'joyo-kanji-code-u.csv')

    def load(self):
        """ Load and return a list of Joyo-Kanji charactors. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class JinmeiKanjiLoader(object):
    """ Jinmeiyou-kanji resource loader class.
    """
    def __init__(self):
        self.delegate = _SingleColInitLoader(__file__,
            'kanji_jinmeiyo', 'jinmei_kanji_code.json', 'jinmeiyou-kanji-code-u.csv')

    def load(self):
        """ Load and return a list of Joyo-Kanji charactors. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class CityLoader(object):
    """ City name resource loader class.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = _SingleColInitLoader(__file__,
            'city', 'city_' + lang + '.json', None)

    def load(self):
        """ Load and return a list of city names """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class CountryLoader(object):
    """ Country resource loader class.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = _SingleColInitLoader(__file__,
            'country', 'country_' + lang + '.json', None)

    def load(self):
        """ Load and return a list of country names. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class NameLoader(object):
    """ Name resource loader class.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = _SingleColInitLoader(__file__,
            'name', 'name_' + lang + '.json', None)

    def load(self):
        """ Load and return a list of names. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class LocationLoader(object):
    """ Location resource loader class.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = _SingleColInitLoader(__file__,
            'location', 'location_' + lang + '.json', 'location_' + lang + '.csv')

    def load(self):
        """ Load and return a list of locations. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

class ThingLoader(object):
    """ Thing resource loader class.
    """
    def __init__(self, lang = 'jpn'):
        self.delegate = _SingleColInitLoader(__file__,
            'thing', 'thing_' + lang + '.json', 'thing_' + lang + '.csv')

    def load(self):
        """ Load and return a list of things. """
        return self.delegate.load()

    def refresh(self):
        self.delegate.refresh()

