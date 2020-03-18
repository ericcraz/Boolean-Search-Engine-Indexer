'''
This is the main module for the search engine portion of the boolean search
engine. This scrip host a console user interface that allows the user to
create a boolean search from the index that was created using the index
creation program. The results are displayed in decreasing score of their
tf-idf score and if they match the boolean query. The time it took to retrive
the information and the amount of results is displayed at the bottom of the
links.
'''

__version__ = '0.1'


import json
import time

from information_class import info_class
from tokinizer import main_tokinizer


def main() -> None:
    '''
    Displays a welcome prompt to the user, retrieves the user's query, checks
    the local cache, retrives the cache if its available if not retrives the
    information from the inverted index on the disk, does some computation
    and displays the results. 
    '''
    welcome_prompt()

    query_list = retrive_query()

    time_start = time.time()

    cache = chech_cache(query_list, time_start)

    if not cache:
        data_list = data_retrival(query_list)

        check_data_display_results(time_start, data_list, query_list)

    ending_prompt()


def chech_cache(query_list: [], time_start: int) -> bool:
    '''
    If the query is already apart of the cache return True and print the urls
    from the cache out. If not, return False.
    '''
    if str(query_list) in info_class.cache:
        time_total = time.time() - time_start

        _print_urls(info_class.cache[str(query_list)], time_total)

        return True

    return False


def check_data_display_results(time_start: int, data_list: [],
                               query_list: []) -> None:
    '''
    Two checks to make sure that the query is valid, first check passes and
    grabs the url results in order from their tf-idf scores, second check
    passes and prints the urls out. If both passes check and the query took
    more than 100 ms, the query and its url data is saved in a local cache
    on disk.
    '''
    if len(data_list) != 0:
        url_list = _results_from_data(data_list)

        if len(url_list) != 0:
            time_total = time.time() - time_start

            _print_urls(url_list, time_total)

            if time_total > .1:
                info_class.save_to_cache(query_list, url_list)
                info_class.save_cache()

        else:
            _no_results()
    else:
        _no_results()


def ending_prompt() -> None:
    '''
    Prints the ending prompt, and asks if the user would like to search again.
    '''
    while True:
        yes_no = input('Would you like to search again?(y/n): ').lstrip().rstrip().lower()

        if yes_no == 'y':
            print()
            break

        elif yes_no == 'n':
            print('Program Exiting')

            return

    main()


def data_retrival(query_list: []) -> []:
    '''
    Retrives the data associated with each query word from their partial index
    on file.
    '''
    token_lists = []

    try:
        for token in query_list:
            with open(info_class.path + token[0] + '.txt') as token_file:
                token_file.seek(info_class.bookkeeping_dict[token])
                line_list = token_file.readline().replace('\n', '').split(' ', 1)

                token_lists.append(json.loads(line_list[1]))

    except KeyError:
        return []

    return token_lists


def retrive_query() -> []:
    '''
    Returns the query after being tokinzed and porter stemmed.
    '''
    query = input('Search: ')

    return main_tokinizer(query)


def welcome_prompt() -> None:
    '''
    Prints the welcome prompt.
    '''
    print('----------------------- Search Engine -----------------------')
    print()


def _print_urls(url_list: [], time_total: int) -> None:
    '''
    Print the url list out using a dictionary in memory, defrags url as well.
    '''
    print()

    for doc_id in url_list:
        url = info_class.index_dict[str(doc_id[0])]
        print(url.split('#')[0])

    print()
    print(f'Search Results: {len(url_list)}')
    print(f'Time: {time_total}')
    print()


def _results_from_data(data_list: []) -> []:
    '''
    This functin carries out the boolean retrival part from the data given. If
    there is more than one result it will be sorted using their tf-idf score
    so the highest score is first.
    '''
    and_check = {}
    url_matches = []

    for doc_list in data_list:
        for doc in doc_list:
            if doc[0] not in and_check:
                and_check[doc[0]] = 1
            else:
                and_check[doc[0]] += 1

            if and_check[doc[0]] == len(data_list):
                url_matches.append(doc)

    if len(url_matches) > 1:
        url_matches.sort(key=lambda x: x[1], reverse=True)

    return url_matches


def _no_results() -> None:
    '''
    Prints a message out letting the user no that their were no results.
    '''
    print()
    print('No Documents Could Be Found With The Given Search')


if __name__ == "__main__":
    '''
    Calls the main function.
    '''
    main()
