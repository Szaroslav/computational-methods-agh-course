import wiki_parser as wp
import redis
from copy import copy
from scipy.sparse import coo_matrix
from mediawiki_dump.tokenizer import clean, tokenize
import nltk
from nltk.corpus import wordnet
from nltk.stem import *
import math
import json
import numpy as np


connection = redis.Redis(host="localhost", port=6379, decode_responses=True)
print(connection.ping())

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


def init():
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
        with open(filename, "r") as file:
            parser = wp.WikiParser(file)

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
    rows, cols, values = [], [], []
    for filename in filenames:
        with open(filename, "r") as file:
            parser = wp.WikiParser(file)

            while (doc := parser.parse_document()) is not None:
                di = {}
                words = tokenize(clean(doc).lower())

                for word in words:
                    word = stemmer.stem(word)
                    if di.get(word) is None:
                        di[word] = 0
                    di[word] += 1
                
                for key in di:
                    if words_dict.get(key) is not None:
                        rows.append(words_dict[key])
                        cols.append(n)
                        values.append(di.get(key))

                n += 1
                # print(n)

    # A = coo_matrix((values, (row, col)), shape=(m, n))
    # IDF = np.empty(m)
    # for i in range(m):
    #     IDF[i] = idf(i)
    # indicies = zip(A.row, A.col)
    # A = A.tocsr()
    # for i, j in indicies:
    #     A[i, j] *= IDF[i]

    print(len(rows))

    with open("dt-sparse.min.json", "w") as file:
        file.write(json.dumps([{ "row": r, "col": c, "value": v } for r, c, v in zip(rows, cols, values)]))

    print(f"{m}, {n}")


init()