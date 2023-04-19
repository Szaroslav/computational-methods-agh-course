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
import json_stream
import storage
from io import TextIOWrapper

if __name__ == "__main__":
    import wiki_parser as wp
else:
    import db.wiki_parser as wp


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


def words_dict(words: list[str]) -> dict[int]:
    words_dict: dict[int] = {}

    for word in words:
        word = stemmer.stem(word)
        if words_dict.get(word) is None:
            words_dict[word] = 0
    
    return words_dict

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


def create():
    filenames: list[str] = [
        "chesswiki.test.xml"
    ]
    n: int = 0
    m: int = 0
    mx, mn = (0, ""), (math.inf, "")
    wd: dict[str, int] = {}

    # for word in tokenize("chess is an abstract board game. playing chess is really fun. king is a chess piece"):
    #     print(stemmer.stem(word))

    def idf(i: int):
        return np.log10(n / doc_f[i])

    #
    # Init dictionary of words occurred at least once in all documents
    #
    print("Initializing dictionary of words...")
    for filename in filenames:
        with open(filename, "r", encoding="utf8") as file:
            parser = wp.WikiParser(file)

            while (doc := parser.parse_document()) is not None:   
                words = tokenize(clean(doc).lower())
                wd.update(words_dict(words))
    
    #
    # Remove stop words from the dictionary
    #
    print("Removing stop words from the dictionary...")
    for word in STOP_WORDS:
        if wd.get(word) is not None:
            wd.pop(word)

    #
    # Set every key of the words dictionary index
    #
    for i, key in enumerate(wd):
        wd[key] = i

    m = len(wd)

    #
    # Iterate over every document available in the dumps
    #
    print("Iterating over every document available in the dumps...")
    rows, cols, values = [], [], []
    doc_f = np.zeros(len(wd))
    for filename in filenames:
        with open(filename, "r", encoding="utf8") as file:
            parser = wp.WikiParser(file)

            while (doc := parser.parse_document()) is not None:
                words = tokenize(clean(doc).lower())
                di = frequency_vector(words)
                doc_f += document_frequency(di, wd)

                r, c, v = sparse_matrix(di, wd, n)
                rows += r
                cols += c
                values += v

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

    # IDF = np.empty(m)
    # for i in range(m):
    #     IDF[i] = idf(i)

    # for k, i in enumerate(rows):
    #     values[k] *= IDF[i]

    print(len(rows))

    with open("dt-sparse.min.json", "w") as file:
        data = [{ "row": r, "col": c, "value": v } for r, c, v in zip(rows, cols, values)]
        file.write(json.dumps({
            "dimensions": { "m": m, "n": n, "sparse_length": len(data) },
            "data": data
        }))

    print(f"{m}, {n}")

def load():
    with open("dt-sparse.min.json", "r", encoding="utf8") as file:
        data = json_stream.load(file)
        storage.sparse_matrix = np.empty(data["dimensions"]["sparse_length"], dtype=storage.dt)
        for i, el in enumerate(data["data"].persistent()):
            storage.sparse_matrix[i]["row"] =  el["row"]
            storage.sparse_matrix[i]["col"] =  el["col"]
            storage.sparse_matrix[i]["value"] =  el["value"]


if __name__ == "__main__":
    load()
    # create()