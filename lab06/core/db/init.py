import os
from copy import copy
from scipy.sparse import coo_matrix
from mediawiki_dump.tokenizer import clean, tokenize
import nltk
from nltk.corpus import wordnet
from nltk.stem import *
import math
import json
import numpy as np
import json_stream
from io import TextIOWrapper
from functools import reduce
from django.core.cache import cache, caches
from scipy.sparse.linalg import svds
from scipy.sparse import csc_array

if __name__ == "__main__":
    import storage as storage
    import wiki_parser as wp
else:
    import db.storage as storage
    import db.wiki_parser as wp

K = 100
CURRENT_PATH = os.path.dirname(__file__)
filenames: list[str] = [
    "chesswiki.test.xml"
]
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


def words_dict(words: list[str]) -> dict[str, int]:
    words_dict: dict[str, int] = {}

    for word in words:
        word = stemmer.stem(word)
        if words_dict.get(word) is None:
            words_dict[word] = 0
    
    return words_dict

def frequency_vector(words: list[str]) -> dict[str, int]:
    frequency_vector: dict[str, int] = {}

    for word in words:
        word = stemmer.stem(word)
        if frequency_vector.get(word) is None:
            frequency_vector[word] = 0
        frequency_vector[word] += 1
    
    return frequency_vector

def sparse_matrix(vector: dict[str, int], words_dict: dict[str, int], j: int) -> tuple[list[int], list[int], list[float]]:
    sparse_matrix: tuple[list[int], list[int], list[float]] = ([], [], [])
    rows, cols, values = sparse_matrix

    for key in vector:
        if words_dict.get(key) is not None:
            rows.append(words_dict[key])
            cols.append(j)
            values.append(vector.get(key))

    return sparse_matrix

def document_frequency(vector: dict[str, int], words_dict: dict[str, int]) -> np.ndarray:
    doc_frequency = np.zeros(len(words_dict))

    for key in vector:
        if words_dict.get(key) is not None:
            doc_frequency[words_dict[key]] += 1

    return doc_frequency

def remove_stop_words(wd: dict[str, int]) -> dict[str, int]:
    print("Removing stop words from the dictionary...")
    for word in STOP_WORDS:
        if wd.get(word) is not None:
            wd.pop(word)

    return wd

def bag_of_words() -> dict[str, int]:
    #
    # Init dictionary of words occurred at least once in all documents
    #
    wd: dict[str, int] = {}

    print("Initializing dictionary of words...")
    for filename in filenames:
        with open(f"{CURRENT_PATH}/{filename}", "r", encoding="utf8") as file:
            parser = wp.WikiParser(file)

            while (doc := parser.parse_document()) is not None:   
                words = tokenize(clean(doc).lower())
                wd.update(words_dict(words))
    
    #
    # Remove stop words from the dictionary
    #
    wd = remove_stop_words(wd)

    #
    # Set every key of the words dictionary index
    #
    for i, key in enumerate(wd):
        wd[key] = i

    return wd


def create():
    n: int = 0
    m: int = 0
    # mx, mn = (0, ""), (math.inf, "") 

    # for word in tokenize("chess is an abstract board game. playing chess is really fun. king is a chess piece"):
    #     print(stemmer.stem(word))

    def idf(i: int):
        return np.log10(n / doc_f[i])

    wd = bag_of_words()
    m = len(wd)

    #
    # Iterate over every document available in the dumps
    #
    print("Iterating over every document available in the dumps...")
    rows, cols, values = [], [], []
    doc_f = np.zeros(len(wd))
    for filename in filenames:
        with open(f"{CURRENT_PATH}/{filename}", "r", encoding="utf8") as file:
            parser = wp.WikiParser(file)

            while (doc := parser.parse_document()) is not None:
                words = tokenize(clean(doc).lower())
                dj = frequency_vector(words)
                doc_f += document_frequency(dj, wd)
                # norm2_dj = reduce(lambda acc, x: acc + x**2, [f for f in dj.values()], 0)**.5
                dj = { key: value for key, value in dj.items() }

                r, c, v = sparse_matrix(dj, wd, n)
                rows += r
                cols += c
                values += v

                n += 1
                # print(n)

    IDF = np.empty(m)
    for i in range(m):
        IDF[i] = idf(i)

    for k, i in enumerate(rows):
        values[k] *= IDF[i]

    print(len(rows))

    with open(f"{CURRENT_PATH}/dt-sparse.min.json", "w") as file:
        data = [{ "row": r, "col": c, "value": v } for r, c, v in zip(rows, cols, values)]
        storage.sparse_matrix = data
        cache.set("sparse_matrix", data)
        file.write(json.dumps({
            "dimensions": { "m": m, "n": n, "sparse_length": len(data) },
            "data": data
        }))

    print(f"{m}, {n}")

def load():
    with open(f"{CURRENT_PATH}/dt-sparse.min.json", "r", encoding="utf8") as file:
        data = json_stream.load(file, persistent=True)

        storage.sparse_matrix_dims = (data["dimensions"]["m"], data["dimensions"]["n"])
        cache.set("sparse_matrix_dims", storage.sparse_matrix_dims)
        norms2 = np.zeros(storage.sparse_matrix_dims[1])

        storage.sparse_matrix = np.empty(data["dimensions"]["sparse_length"], dtype=storage.dt)
        for i, el in enumerate(data["data"]):
            storage.sparse_matrix[i]["row"]     = el["row"]
            storage.sparse_matrix[i]["col"]     = el["col"]
            storage.sparse_matrix[i]["value"]   = el["value"]
            norms2[el["col"]]                  += el["value"]**2

        storage.bow = bag_of_words()
        cache.set("bag_of_words", storage.bow)

        if K is not None and K >= 1:
            m, n = storage.sparse_matrix_dims
            rows, cols, values = [], [], []
            for el in storage.sparse_matrix:
                rows.append(el["row"])
                cols.append(el["col"])
                values.append(el["value"])
            storage.scipy_s_matrix = csc_array((values, (rows, cols)), shape=(m, n))
            storage.U, storage.D, storage.V = svds(storage.scipy_s_matrix, k=K)

            S = np.zeros((K, n))
            storage.S = S
            for i in range(K):
                for j in range(n):
                    S[i][j] = storage.D[i] * storage.V[i][j]

        if K is not None and K >= 1:
            norms2 = np.zeros(n)
            for i in range(K):
                for j in range(n):
                    norms2[j] += S[i][j]**2
            norms2 = np.array([n**.5 for n in norms2])

            for i in range(K):
                for j in range(n):
                    S[i][j] /= norms2[j]
            cache.set("S", storage.S)
        else:
            norms2 = np.array([n**.5 for n in norms2])
            for i in range(len(storage.sparse_matrix)):
                storage.sparse_matrix[i]["value"] /= norms2[el["col"]]
            cache.set("sparse_matrix", storage.sparse_matrix)


if __name__ == "__main__":
    # load()
    create()