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

# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()


def frequency_vector(words: list[str]) -> dict[int]:
    frequency_vector: dict[int] = {}

    for word in words:
        word = stemmer.stem(word)
        if frequency_vector.get(word) is None:
            frequency_vector[word] = 0
        frequency_vector[word] += 1
    
    return frequency_vector


def sparse_matrix(vector: dict[int], words_dict: dict[int], j: int) -> tuple[list[int], list[int], list[float]]:
    sparse_matrix: tuple[list[int], list[int], list[float]] = ([], [], [])
    rows, cols, values = sparse_matrix

    for key in vector:
        if words_dict.get(key) is not None:
            rows.append(words_dict[key])
            cols.append(j)
            values.append(vector.get(key))

    return sparse_matrix


def document_frequency(vector: dict[int], words_dict: dict[int]) -> np.ndarray:
    doc_frequency = np.zeros(len(words_dict))

    for key in vector:
        if words_dict.get(key) is not None:
            doc_frequency[words_dict[key]] += 1

    return doc_frequency


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

    # for word in tokenize("chess is an abstract board game. playing chess is really fun. king is a chess piece"):
    #     print(stemmer.stem(word))

    def idf(i: int):
        return np.log10(n / doc_f[i])

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
    doc_f = None
    for filename in filenames:
        with open(filename, "r") as file:
            parser = wp.WikiParser(file)

            while (doc := parser.parse_document()) is not None:
                words = tokenize(clean(doc).lower())
                di = frequency_vector(words)
                rows, cols, values = sparse_matrix(di, words_dict, n)
                doc_f = document_frequency(di, words_dict)

                n += 1
                # print(n)

    # A = coo_matrix((values, (rows, cols)), shape=(m, n))
    # IDF = np.empty(m)
    # for i in range(m):
    #     IDF[i] = idf(i)
    # indicies = zip(A.row, A.col)
    # A = A.tocsr()
    # for i, j in indicies:
    #     A[i, j] *= IDF[i]

    IDF = np.empty(m)
    for i in range(m):
        IDF[i] = idf(i)

    for k, i in enumerate(rows):
        values[k] *= IDF[i]

    print(len(rows))

    with open("dt-sparse.json", "w") as file:
        file.write(json.dumps([{ "row": r, "col": c, "value": v } for r, c, v in zip(rows, cols, values)], indent=4))

    print(f"{m}, {n}")


init()