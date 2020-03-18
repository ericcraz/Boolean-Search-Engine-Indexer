'''
This is the main module for the index creation portion of the boolean search
engine. This script grabs all file paths in the "DEV" directory
(all files must be .json and must be web pages including html), then continues
to parse one file at time, saving an inverted index into memory until one of
the three break points has been hit, which will then offload the current
inverted index into a partial inverted index onto disk, and finally the
three partial indexes will be merged into the final partial indexes.

Third party libraries: lxml and BeautifulSoup.
'''

__version__ = '0.1'


import json
import re
import math

from information_save import info_class
from tokinizer import main_tokinizer
from bs4 import BeautifulSoup
from os import listdir


def main() -> None:
    '''
    Grabs the file paths from the DEV directory, creates the three partial
    indexes on disk, merges the partial indexes into a final partial
    indexes on disk and finally saves some important information in
    regards to the index and statistics.
    '''
    file_paths = get_file_paths()

    create_indexes(file_paths)

    merge_indexes()

    information_save()


def create_indexes(file_paths: []) -> None:
    '''
    For loops through all of the file paths, loads the file, tokinizes the
    file, creates a partial index and then offloads the partial index
    from memory to the disk at three breakpoints.
    '''
    break_points = _break_points(len(file_paths))

    index = 0

    for file_path in file_paths:
        json_obj = json.load(open(file_path))

        important_text = _important_text(json_obj)

        token_dict = main_tokinizer(important_text)

        index_words(token_dict, index)
        _unique_words_add(list(token_dict.keys()))
        info_class.url_dict[index] = json_obj['url']

        index += 1

        if index in break_points:
            save_partial_index(break_points.index(index))

        print(f'File: {index}')

        # DEBUGGING
        if index == 0:
            pass  # Change to break in case of debugging purposes
        # DEBUGGING


def save_partial_index(partial_index_int: int) -> None:
    '''
    This function will take in a partial index in the form of a dictionary,
    this then saves the index into a .txt file onto the disk,
    and finally clears the index in memory.
    '''
    path = info_class.index_dir + 'partial_index_' + str(partial_index_int) + '.txt'

    current_line = '0'

    with open(path, 'w') as current_file:
        for word in sorted(info_class.index_dict.keys()):
            first_char = word[0]

            if current_line != first_char:
                current_line = first_char

                current_file.write('\n' + word + ';' +
                                   str(info_class.index_dict[word]) + '|')
            else:
                current_file.write(word + ';' +
                                   str(info_class.index_dict[word]) + '|')

    info_class.index_dict.clear()


def index_words(token_dict: {}, url: str) -> None:
    '''
    Takes in a dictionary of the tokens and their frequency, computes the term
    frequency, checks to see if the word is important and finally saves the
    word and its inverted index into a dictionary inside of memory.
    '''
    for word in token_dict:
        tf = token_dict[word]/len(token_dict)

        important = 0

        if word in info_class.important_words_dict:
            important = 1

        if word not in info_class.index_dict:
            info_class.index_dict[word] = [[url, tf, important]]
        else:
            info_class.index_dict[word].append([url, tf, important])


def get_file_paths() -> []:
    '''
    Grabs all the file paths from the DEV directory and return them inside a
    list.
    '''
    file_paths = []

    for folder in listdir(info_class.dev_dir):
        for file_name in listdir(info_class.dev_dir + folder):
            file_paths.append(info_class.dev_dir + folder + '/' + file_name)

    return file_paths


def information_save() -> None:
    '''
    Saves two in memory dictionarys used as a index search up for the query to
    .json files, one file is simply the count of unique words found.
    '''
    json.dump(len(info_class.unique_words_dict),
              open(info_class.index_dir + 'unique_words.json', 'w'))

    json.dump(info_class.url_dict,
              open(info_class.index_dir + 'index_directory.json', 'w'))

    json.dump(info_class.bookkeeping_dict,
              open(info_class.index_dir + 'bookkeeping_dict.json', 'w'))


def merge_indexes() -> None:
    '''
    This functions loads all three partial indexes and for loops through their
    lines all at the same time. Grabbing the infromation from the line and
    passing it to another function to merge/parse.
    '''
    path_one = info_class.index_dir + info_class.partial_index_file_paths[0]
    path_two = info_class.index_dir + info_class.partial_index_file_paths[1]
    path_three = info_class.index_dir + info_class.partial_index_file_paths[2]

    with open(path_one) as partial_one:
        with open(path_two) as partial_two:
            with open(path_three) as partial_three:
                for _ in range(62):
                    line_one = partial_one.readline()
                    line_two = partial_two.readline()
                    line_three = partial_three.readline()

                    _save_to_file(line_one[0],
                                  [line_one, line_two, line_three])


def _save_to_file(file_name: str, lines: []) -> None:
    '''
    Parses the lines given and then creates a dictionary of all contents in
    memory, for each word the tf-idf is caculated and then finally saved to
    their partial index.
    '''
    path = info_class.final_index_dir + file_name + '.txt'

    current_dict = {}

    for line in lines:  # for current line
        split_by_word = line.split('|')[0:-1]

        for word in split_by_word:  # for word in current line
            split_by_word = word.split(';')  # split_by_word[0] == the word
            word_list = json.loads(split_by_word[1])  # the word list

            if split_by_word[0] not in current_dict:
                current_dict[split_by_word[0]] = word_list
            else:
                for doc_info in word_list:
                    current_dict[split_by_word[0]].append(doc_info)

    char_count = 0

    with open(path, 'w') as current_file:
        for word in current_dict:
            word_list = _tf_idf(current_dict[word])

            info_class.bookkeeping_dict[word] = char_count

            char_count = char_count + len(word) + len(str(word_list)) + 3

            current_file.write(word + ' ' + str(word_list) + '\n')


def _tf_idf(word_list: []) -> []:
    '''
    Caculates the tf-idf of the given word and their data, then replaces their
    data with the tf-idf score.
    '''
    idf = math.log10(55393/(len(word_list) + 1))

    new_word_list = []

    for doc in word_list:
        tf_idf = idf * doc[1]

        if doc[2] == 1:
            tf_idf += .1

        if tf_idf > 1:
            tf_idf = 1

        new_word_list.append([doc[0], tf_idf])

    return new_word_list


def _unique_words_add(token_list: []) -> None:
    '''
    Adds a word to a dictionary if it has not been seen already.
    '''
    for key in token_list:
        if key not in info_class.unique_words_dict:
            info_class.unique_words_dict[key] = None


def _important_text(json_obj) -> str:
    '''
    This function takes in a json_obj of a web page that has been opened, this
    will parse it using beautiful soup and lxml. Replaces certian characters,
    grabs the important text and returns it.
    '''
    soup = BeautifulSoup(json_obj['content'], 'lxml')

    important_text = soup.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
    important_text_short = important_text[0:4000]

    _important_words(soup)

    return important_text_short


def _break_points(list_length: int) -> [int]:
    '''
    This function finds the three break points to allow for offloading the
    inverted index, the breakpoints are returned as ints inside a list.
    '''
    first = int(list_length/3)
    second = first * 2
    third = list_length - 1

    return [first, second, third]


def _important_words(soup) -> None:
    '''
    Parsing through the html using beautiful soup this grabs all the
    "important words" and saves it in a dictionary,
    this dictionary is used per file.
    '''
    info_class.important_words_dict.clear()

    h1_text = soup.find_all('h1')
    h2_text = soup.find_all('h2')
    h3_text = soup.find_all('h3')
    h4_text = soup.find_all('h4')
    h5_text = soup.find_all('h5')
    h6_text = soup.find_all('h6')
    strong_text = soup.find_all('strong')
    bold_text = soup.find_all('bold')
    title_text = soup.find_all('title')

    all_text = [h1_text, h2_text, h3_text, h4_text, h5_text, h6_text,
                strong_text, bold_text, title_text]

    for text_list in all_text:
        if len(text_list) != 0:
            for text_string in text_list:
                try:
                    just_text = str(text_string).replace('\n', '').replace('\r', '').replace('\t', '')
                    just_text = re.split(r'(>)(.+)(<)', just_text)[2]

                    text_list = list(main_tokinizer(just_text).keys())

                    for token in text_list:
                        if token not in info_class.important_words_dict:
                            info_class.important_words_dict[token] = None
                except IndexError:
                    pass


if __name__ == "__main__":
    '''
    Calls the main function.
    '''
    main()
