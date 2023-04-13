from django.shortcuts import render
from django.http import HttpResponse
from .wiki_parser import WikiParser
from copy import copy
import math

# Create your views here.
def init(request):
    WIKI_FILE_PATH = "/home/szary/Downloads/wiki/"
    CONTENT_TAG_NAME = "text"
    OPENING_TAG, CLOSING_TAG = f"<{CONTENT_TAG_NAME}", f"</{CONTENT_TAG_NAME}>"
    filenames: list[str] = [
        "simplewiki-20230401-pages-articles-multistream.xml",
        # "enwiki-20230401-pages-articles-multistream1.xml-p1p41242",
        # "enwiki-20230401-pages-articles-multistream2.xml-p41243p151573",
        # "enwiki-20230401-pages-articles-multistream3.xml-p151574p311329"
    ]
    count: int = 0
    mx, mn = (0, ""), (math.inf, "")
    bag_of_words: dict[str, int] = {}
    words_base: list[str] = []

    # Init dictionary of words occurred at least once in all documents
    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            while (words := parser.parse_line()) is not None:            
                for word in words:
                    if bag_of_words.get(word) is None:
                        bag_of_words[word] = 0
            # for key in bag_of_words:
            #     if bag_of_words[key] > mx[0]:
            #         mx = (bag_of_words[key], key)
            #     elif bag_of_words[key] < mn[0]:
            #         mn = (bag_of_words[key], key)

    words_base = copy(list(bag_of_words.keys()))

    # Iterate document-wise over files
    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            while (words := parser.parse_document()) is not None and len(words) > 0:    
                di = copy(bag_of_words)

                for word in words:
                    if bag_of_words.get(word) is None:
                        bag_of_words[word] = 0
                    bag_of_words[word] += 1

    return HttpResponse(f"Length: {len(bag_of_words)}")
