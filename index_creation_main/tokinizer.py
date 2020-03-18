'''
This module is the tokinzer that parses text from the web pages. This file
takes in html content as a string, finds the word frequency and porter stems
the words. This file returns a dictionary with the keys being the words and
the values being their frequencies.

Third party libraries: NLTK.
'''


import re

from nltk.stem import PorterStemmer


def main_tokinizer(html_content: str) -> {}:
    '''
    This is the main function. Takes in html content, tokinizes the content
    and then returns a dictionary with the token as a key and the frequency
    as the value.
    '''
    token_dict = tokinize_content(html_content)

    return token_dict


def tokinize_content(html_content: str) -> {}:
    '''
    Takes in html content and tokinizes. Returns a dictionary of the words
    tokinized and their frequencies.
    '''
    tokinized_dict = {}

    _tokinize_content(html_content, tokinized_dict)

    return tokinized_dict


def _tokinize_content(current_line: str, tokinized_dict: {}) -> None:
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

        if stemed_string in tokinized_dict:
            tokinized_dict[stemed_string] += 1
        else:
            tokinized_dict[stemed_string] = 1
