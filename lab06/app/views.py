from django.shortcuts import render
from django.http import HttpResponse
from .wiki_parser import WikiParser
from copy import copy
from scipy.sparse import coo_matrix
import math
import numpy as np


def init(request):
    WIKI_FILE_PATH = "/home/szary/Downloads/wiki/"
    CONTENT_TAG_NAME = "text"
    OPENING_TAG, CLOSING_TAG = f"<{CONTENT_TAG_NAME}", f"</{CONTENT_TAG_NAME}>"
    filenames: list[str] = [
        "simplewiki.xml",
        # "simplewiki-20230401-pages-articles-multistream.xml",
        # "enwiki-20230401-pages-articles-multistream1.xml,
        # "enwiki-20230401-pages-articles-multistream2.xml",
        # "enwiki-20230401-pages-articles-multistream3.xml"
    ]
    count: int = 0
    n: int = 0
    m: int = 0
    mx, mn = (0, ""), (math.inf, "")
    bag_of_words: dict[str, int] = {}
    words_base: list[str] = []

    def idf(i: int):
        return np.log10(n / A.getrow(i).getnnz(1))

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
    row, col, values = [], [], []
    for filename in filenames:
        with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

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

    A = coo_matrix((values, (row, col)), shape=(m, n))
    IDF = np.empty(m)
    for i in range(m):
        IDF[i] = idf(i)
    indicies = zip(A.row, A.col)
    A = A.tocsr()
    for i, j in indicies:
        A[i, j] *= IDF[i]

    return HttpResponse(f"{m}, {n}")

def create_file(request):
    WIKIS_FILE_PATH = "/run/media/szary/SanDisk/"

    filenames: list[str] = [
        # "enwiki-20230401-pages-articles-multistream1.xml",
        # "enwiki-20230401-pages-articles-multistream2.xml",
        # "enwiki-20230401-pages-articles-multistream3.xml",
        # "enwiki-20230401-pages-articles-multistream4.xml",
        # "enwiki-20230401-pages-articles-multistream5.xml",
        # "enwiki-20230401-pages-articles-multistream6.xml",
        # "enwiki-20230401-pages-articles-multistream7.xml",
        # "enwiki-20230401-pages-articles-multistream8.xml",
        # "enwiki-20230401-pages-articles-multistream9.xml",
        # "enwiki-20230401-pages-articles-multistream10.xml",
        # "enwiki-20230401-pages-articles-multistream11.1.xml",
        # "enwiki-20230401-pages-articles-multistream11.2.xml",
        # "enwiki-20230401-pages-articles-multistream12.1.xml",
        # "enwiki-20230401-pages-articles-multistream12.2.xml",
        # "enwiki-20230401-pages-articles-multistream13.1.xml",
        # "enwiki-20230401-pages-articles-multistream13.2.xml",
        # "enwiki-20230401-pages-articles-multistream14.1.xml",
        # "enwiki-20230401-pages-articles-multistream14.2.xml",
        # "enwiki-20230401-pages-articles-multistream15.1.xml",
        # "enwiki-20230401-pages-articles-multistream15.2.xml",
        # "enwiki-20230401-pages-articles-multistream15.3.xml",
        # "enwiki-20230401-pages-articles-multistream16.1.xml",
        # "enwiki-20230401-pages-articles-multistream16.2.xml",
        # "enwiki-20230401-pages-articles-multistream16.3.xml",
        # "enwiki-20230401-pages-articles-multistream17.1.xml",
        # "enwiki-20230401-pages-articles-multistream17.2.xml",
        # "enwiki-20230401-pages-articles-multistream17.3.xml",
        # "enwiki-20230401-pages-articles-multistream18.1.xml",
        # "enwiki-20230401-pages-articles-multistream18.2.xml",
        # "enwiki-20230401-pages-articles-multistream18.3.xml",
        # "enwiki-20230401-pages-articles-multistream19.1.xml",
        # "enwiki-20230401-pages-articles-multistream19.2.xml",
        # "enwiki-20230401-pages-articles-multistream19.3.xml",
        # "enwiki-20230401-pages-articles-multistream20.1.xml",
        # "enwiki-20230401-pages-articles-multistream20.2.xml",
        # "enwiki-20230401-pages-articles-multistream20.3.xml",
        "enwiki-20230401-pages-articles-multistream21.1.xml",
        "enwiki-20230401-pages-articles-multistream21.2.xml",
        "enwiki-20230401-pages-articles-multistream21.3.xml",
        "enwiki-20230401-pages-articles-multistream22.1.xml",
        "enwiki-20230401-pages-articles-multistream22.2.xml",
        "enwiki-20230401-pages-articles-multistream22.3.xml",
        "enwiki-20230401-pages-articles-multistream22.4.xml",
        "enwiki-20230401-pages-articles-multistream23.1.xml",
        "enwiki-20230401-pages-articles-multistream23.2.xml",
        "enwiki-20230401-pages-articles-multistream23.3.xml",
        "enwiki-20230401-pages-articles-multistream23.4.xml",
        "enwiki-20230401-pages-articles-multistream24.1.xml",
        "enwiki-20230401-pages-articles-multistream24.2.xml",
        "enwiki-20230401-pages-articles-multistream24.3.xml",
        "enwiki-20230401-pages-articles-multistream24.4.xml",
        "enwiki-20230401-pages-articles-multistream24.5.xml",
        "enwiki-20230401-pages-articles-multistream25.1.xml",
        "enwiki-20230401-pages-articles-multistream25.2.xml",
        "enwiki-20230401-pages-articles-multistream25.3.xml",
        "enwiki-20230401-pages-articles-multistream25.4.xml",
        "enwiki-20230401-pages-articles-multistream26.1.xml",
        "enwiki-20230401-pages-articles-multistream27.1.xml",
        "enwiki-20230401-pages-articles-multistream27.2.xml",
        "enwiki-20230401-pages-articles-multistream27.3.xml",
        "enwiki-20230401-pages-articles-multistream27.4.xml",
        "enwiki-20230401-pages-articles-multistream27.5.xml",
        "enwiki-20230401-pages-articles-multistream27.6.xml",
        "enwiki-20230401-pages-articles-multistream27.7.xml"
    ]

    # for filename in filenames:
    #     with open(f"{WIKI_FILE_PATH}{filename}", "r") as file:
    #         with open(f"{WIKI_FILE_PATH}simplewiki.xml", "w") as file0:
    #             for i, line in enumerate(file):
    #                 if i == 200000:
    #                     break

    #                 file0.write(line)
    c = 0
    for filename in filenames:
        with open(f"{WIKIS_FILE_PATH}{filename}", "r") as file:
            with open(f"/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/chesswiki.xml", "a") as file0:
                parser = WikiParser(file)

                while (document := parser.get_document()) is not None:
                    pass
                    if "chess" in document:
                        c += 1
                        file0.write(document)

    return HttpResponse(c)

def count(request):
    c = 0
    with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/chesswiki.xml", "r") as file:
        c = WikiParser(file).count()

    return HttpResponse(c)