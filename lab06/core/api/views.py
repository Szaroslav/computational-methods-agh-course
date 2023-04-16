from django.shortcuts import render
from django.http import HttpResponse
from .wiki_parser import WikiParser
from copy import copy
from scipy.sparse import coo_matrix
from mediawiki_dump.tokenizer import clean, tokenize
import nltk
from nltk.corpus import wordnet
from nltk.stem import *
import math
import numpy as np


STOP_WORDS = [
    "a",
    "about",
    "actually",
    "almost",
    "also",
    "although",
    "always",
    "am",
    "an",
    "and",
    "any",
    "are",
    "as",
    "at",
    "be",
    "became",
    "become",
    "but",
    "by",
    "can",
    "could",
    "did",
    "do",
    "does",
    "each",
    "either",
    "else",
    "for",
    "from",
    "had",
    "has",
    "have",
    "hence",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "its",
    "just",
    "may",
    "maybe",
    "me",
    "might",
    "mine",
    "must",
    "my",
    "mine",
    "must",
    "my",
    "neither",
    "nor",
    "not",
    "of",
    "oh",
    "ok",
    "when",
    "where",
    "whereas",
    "wherever",
    "whenever",
    "whether",
    "which",
    "while",
    "who",
    "whom",
    "whoever",
    "whose",
    "why",
    "will",
    "with",
    "within",
    "without",
    "would",
    "yes",
    "yet",
    "you",
    "your"
]


def init(request):
    WIKIS_FILE_PATH = "/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/core/db/"
    CONTENT_TAG_NAME = "text"
    OPENING_TAG, CLOSING_TAG = f"<{CONTENT_TAG_NAME}", f"</{CONTENT_TAG_NAME}>"
    filenames: list[str] = [
        "chesswiki.test.xml"
    ]
    count: int = 0
    n: int = 0
    m: int = 0
    mx, mn = (0, ""), (math.inf, "")
    words_dict: dict[str, int] = {}
    words_base: list[str] = []

    # nltk.download('wordnet')
    # nltk.download('punkt')
    # nltk.download('averaged_perceptron_tagger')
    # lemmatizer = WordNetLemmatizer()
    stemmer = PorterStemmer()

    def idf(i: int):
        return np.log10(n / A.getrow(i).getnnz(1))

    def get_poses(words: list[str]):
        tag_dict = {
            "J": wordnet.ADJ,
            "N": wordnet.NOUN,
            "V": wordnet.VERB,
            "R": wordnet.ADV
        }
        tags = nltk.pos_tag(words)

        return [tag_dict.get(tag[1][0].upper(), wordnet.NOUN) for tag in tags]

    #
    # Init dictionary of words occurred at least once in all documents
    #
    print("Initializing dictionary of words...")
    for filename in filenames:
        with open(f"{WIKIS_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            while (doc := parser.parse_document()) is not None:   
                words = tokenize(clean(doc).lower())
                for word in words:
                    word = stemmer.stem(word)
                    if words_dict.get(word) is None:
                        words_dict[word] = 0
                pass
    
    #
    # Remove stop words from the dictionary
    #
    print("Removing stop words from the dictionary...")
    for word in STOP_WORDS:
        if words_dict.get(word) is not None:
            words_dict.pop(word)

    #
    # Set every key of the words dictionary index
    #
    for i, key in enumerate(words_dict):
        words_dict[key] = i

    m = len(words_dict)

    #
    # Iterate over every document available in the dumps
    #
    print("Iterating over every document available in the dumps...")
    row, col, values = [], [], []
    for filename in filenames:
        with open(f"{WIKIS_FILE_PATH}{filename}", "r") as file:
            parser = WikiParser(file)

            while (doc := parser.parse_document()) is not None:
                di = {}
                words = tokenize(clean(doc).lower())
                # poses = get_poses(words)

                for word in words:
                    word = stemmer.stem(word)
                    if di.get(word) is None:
                        di[word] = 0
                    di[word] += 1
                
                # for key in di:
                #     if di.get(key) > 0 and words_dict.get(key) is not None:
                #         row.append(words_dict[key])
                #         col.append(n)
                #         values.append(di.get(key))

                n += 1
                print(n)

    # A = coo_matrix((values, (row, col)), shape=(m, n))
    # IDF = np.empty(m)
    # for i in range(m):
    #     IDF[i] = idf(i)
    # indicies = zip(A.row, A.col)
    # A = A.tocsr()
    # for i, j in indicies:
    #     A[i, j] *= IDF[i]

    return HttpResponse(f"{m}, {n}")

def create_file(request):
    WIKIS_FILE_PATH = "/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/core/db/"

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
        # "enwiki-20230401-pages-articles-multistream21.1.xml",
        # "enwiki-20230401-pages-articles-multistream21.2.xml",
        # "enwiki-20230401-pages-articles-multistream21.3.xml",
        # "enwiki-20230401-pages-articles-multistream22.1.xml",
        # "enwiki-20230401-pages-articles-multistream22.2.xml",
        # "enwiki-20230401-pages-articles-multistream22.3.xml",
        # "enwiki-20230401-pages-articles-multistream22.4.xml",
        # "enwiki-20230401-pages-articles-multistream23.1.xml",
        # "enwiki-20230401-pages-articles-multistream23.2.xml",
        # "enwiki-20230401-pages-articles-multistream23.3.xml",
        # "enwiki-20230401-pages-articles-multistream23.4.xml",
        # "enwiki-20230401-pages-articles-multistream24.1.xml",
        # "enwiki-20230401-pages-articles-multistream24.2.xml",
        # "enwiki-20230401-pages-articles-multistream24.3.xml",
        # "enwiki-20230401-pages-articles-multistream24.4.xml",
        # "enwiki-20230401-pages-articles-multistream24.5.xml",
        # "enwiki-20230401-pages-articles-multistream25.1.xml",
        # "enwiki-20230401-pages-articles-multistream25.2.xml",
        # "enwiki-20230401-pages-articles-multistream25.3.xml",
        # "enwiki-20230401-pages-articles-multistream25.4.xml",
        # "enwiki-20230401-pages-articles-multistream26.1.xml",
        # "enwiki-20230401-pages-articles-multistream27.1.xml",
        # "enwiki-20230401-pages-articles-multistream27.2.xml",
        # "enwiki-20230401-pages-articles-multistream27.3.xml",
        # "enwiki-20230401-pages-articles-multistream27.4.xml",
        # "enwiki-20230401-pages-articles-multistream27.5.xml",
        # "enwiki-20230401-pages-articles-multistream27.6.xml",
        # "enwiki-20230401-pages-articles-multistream27.7.xml"
    ]

    with open(f"{WIKIS_FILE_PATH}chesswiki.xml", "r") as file:
        with open(f"{WIKIS_FILE_PATH}chesswiki.test.xml", "w") as file0:
            for i, line in enumerate(file):
                if i == 500000:
                    break

                file0.write(line)

    # for filename in filenames:
    #     with open(f"{WIKIS_FILE_PATH}{filename}", "r") as file:
    #         with open(f"/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/chesswiki.xml", "a") as file0:
    #             parser = WikiParser(file)

    #             while (document := parser.get_document()) is not None:
    #                 pass
    #                 if "chess" in document:
    #                     file0.write(document)

    return HttpResponse()

def count(request):
    c = 0
    with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/core/chesswiki.xml", "r") as file:
        c = WikiParser(file).count()

    return HttpResponse(c)