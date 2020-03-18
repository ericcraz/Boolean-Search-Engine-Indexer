# Boolean Search Engine & Indexer
> A search engine that can index a corpus of web pages under harsh operational constraints and having a query response under 300ms.


This program has two parts, an indexer and a search engine. They work together to create a search engine that can retrive web pages in under 100ms. For example this project was built using 55,000 web pages (5.4GB) and is able to index these using porter steming, checking for important words, and calculating the tf-idf while offloading indexes from memory onto disk and finally merging them together from the disk in under 25 min. 

## Installation

OS X & Linux & Windows:

```sh
User must download program directory
```

## Usage example

Can create an inverted index of a large corpus in a short amount of time while not keeping the inverted index in memory, this allows computers with a small amount of RAM to still be able to index a very large corpus of web pages. Then using the console interface one can create a query that will then present all the boolean url matches of the said query in decreasing order of their tf-idf score.

## Development setup

For this program to run correctly you must install these three dependencies. If you have trouble please troubleshoot with google. The three libraries are: nltk, lxml, and beautifulsoup. 

```sh
pip install nltk
```

```sh
pip install lxml
```

```sh
pip install beautifulsoup4
```

## Directions for use

1. Download the directory and go inside the index_creation_main directory.
2. Put your corpus of .json files inside the empty "DEV" folder, the .json files must have the header fields "url" and "content". NOTE: the "url" header should include the url of the web page and the "content" header should include the html of the page.
3. Using the command line run the main.py file still inside the index_creation_main directory. The file number will be displayed on the console.
4. Once the indexer has finished you may go over to the boolean_search_main directory and run the main.py file.
5. You may now use the console UI to search queries.

## Release History

* 0.1.0
    * The first proper release

## Meta

Eric Chambers –  chambersderic@gmail.com

Distributed under the Apache License. See ``LICENSE`` for more information.

## Contributing

1. Fork it (<https://github.com/ericcraz/Boolean-Search-Engine-Indexer/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
