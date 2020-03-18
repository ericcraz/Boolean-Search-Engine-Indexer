'''
This module is a helper class that aids the search engines functionality.
'''

import json
import pathlib


class information_class():
    def __init__(self) -> None:
        self.path = str(pathlib.Path(__file__).parent.absolute()) + r'\\indexes\\'
        self.bookkeeping_dict = self._load_bookeeping_dict()
        self.index_dict = self._load_index_dict()
        self.cache = self._load_cache()

    def save_cache(self) -> None:
        json.dump(self.cache, open(self.path + 'cache.json', 'w'))

    def save_to_cache(self, query_list: [], url_list: []):
        self.cache[str(query_list)] = url_list

    def _load_cache(self) -> {}:
        cache = json.load(open(self.path + 'cache.json'))
        return cache

    def _load_index_dict(self) -> {}:
        index = json.load(open(self.path + 'index_directory.json'))
        return index

    def _load_bookeeping_dict(self) -> {}:
        index = json.load(open(self.path + 'bookkeeping_dict.json'))
        return index


info_class = information_class()
