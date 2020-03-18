'''
This module is the same as the tokinizer.py inside of the index_creation_main
directory with slight modifications to increase performance and remove certian
detials that is not needed in the search engine part of this program.
'''


import re

from nltk.stem import PorterStemmer


def main_tokinizer(content: str) -> {}:
    '''
    This is the main function. Takes in content, tokinizes the content
    and then returns a list of the keys.
    '''
    token_dict = tokinize_content(content)

    return list(token_dict.keys())


def tokinize_content(content: str) -> {}:
    '''
    Takes in content and tokinizes. Returns a dictionary of the words
    tokinized.
    '''
    tokinized_dict = {}

    _tokinize_line(content, tokinized_dict)

    return tokinized_dict


def _tokinize_line(current_line: str, tokinized_dict: {}) -> None:
    '''
    Takes in a string and a dict that is either empty or has keys and values
    representing the tokens. Splits the line by alphanumeric strings, stems
    them using porter stemming and then puts them inside the dictionary.
    Returns nothing.
    '''
    pattern = [r'[a-zA-Z0-9]+']

    tokens_list = re.findall(pattern[0], current_line)
    ps = PorterStemmer()

    for string in tokens_list:
        stemed_string = ps.stem(string)

        if stemed_string not in tokinized_dict:
            tokinized_dict[stemed_string] = None
