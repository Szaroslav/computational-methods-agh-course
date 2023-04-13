from django.shortcuts import render
from django.http import HttpResponse
from .wiki_parser import WikiParser
from copy import copy
from scipy.sparse import bsr_array
import math
import numpy as np

# Create your views here.
def init(request):
    WIKI_FILE_PATH = "/home/szary/Downloads/wiki/"
    CONTENT_TAG_NAME = "text"
    OPENING_TAG, CLOSING_TAG = f"<{CONTENT_TAG_NAME}", f"</{CONTENT_TAG_NAME}>"
    filenames: list[str] = [
        "simplewiki.xml",
        # "simplewiki-20230401-pages-articles-multistream.xml",
        # "enwiki-20230401-pages-articles-multistream1.xml-p1p41242",
        # "enwiki-20230401-pages-articles-multistream2.xml-p41243p151573",
        # "enwiki-20230401-pages-articles-multistream3.xml-p151574p311329"
    ]
    count: int = 0
    n: int = 0
    m: int = 0
    mx, mn = (0, ""), (math.inf, "")
    bag_of_words: dict[str, int] = {}
    words_base: list[str] = []

    #
    # Init dictionary of words occurred at least once in all documents
    #
    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            while (words := parser.parse_line()) is not None:            
                for word in words:
                    if bag_of_words.get(word) is None:
                        bag_of_words[word] = 0

    words_base = copy(list(bag_of_words.keys()))
    m = len(words_base)

    #
    # Iterate document-wise over files
    #
    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            row, col, values = [], [], []
            
            while (words := parser.parse_document()) is not None:    
                di = copy(bag_of_words)

                for word in words:
                    if di.get(word) is not None:
                        di[word] += 1
                
                for i, key in enumerate(di):
                    if di.get(key) > 0:
                        row.append(i)
                        col.append(n)
                        values.append(di.get(key))

                n += 1

        A = bsr_array((values, (row, col)), shape=(m, n))

    return HttpResponse(f"{m}, {n}")

def create_file(request):
    WIKI_FILE_PATH = "/home/szary/Downloads/wiki/"
    filenames: list[str] = [
        "simplewiki-20230401-pages-articles-multistream.xml"
    ]

    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            with open(f"{WIKI_FILE_PATH}simplewiki.xml", "w") as file0:
                for i, line in enumerate(file):
                    if i == 200000:
                        break

                    file0.write(line)

    return HttpResponse()