import unittest as ut
from mediawiki_dump.tokenizer import tokenize
import api.search as sr
import numpy as np


class TestSearch(ut.TestCase):
    sentences = [
        "Chess is an abstract board game.",
        "Playing chess is really fun. Chess.",
        "King is a chess piece."
    ]
    sparse_matrix = [
        { "row": 0, "col": 0, "value": 1 },
        { "row": 1, "col": 0, "value": 1 },
        { "row": 2, "col": 0, "value": 1 },
        { "row": 3, "col": 0, "value": 1 },
        { "row": 0, "col": 1, "value": 2 },
        { "row": 4, "col": 1, "value": 1 },
        { "row": 5, "col": 1, "value": 1 },
        { "row": 6, "col": 1, "value": 1 },
        { "row": 0, "col": 2, "value": 1 },
        { "row": 7, "col": 2, "value": 1 },
        { "row": 8, "col": 2, "value": 1 }
    ]
    normalized_sparse_matrix = [
        { "row": 0, "col": 0, "value": 1 / 2 },
        { "row": 1, "col": 0, "value": 1 / 2 },
        { "row": 2, "col": 0, "value": 1 / 2 },
        { "row": 3, "col": 0, "value": 1 / 2 },
        { "row": 0, "col": 1, "value": 2 / 7**.5 },
        { "row": 4, "col": 1, "value": 1 / 7**.5 },
        { "row": 5, "col": 1, "value": 1 / 7**.5 },
        { "row": 6, "col": 1, "value": 1 / 7**.5 },
        { "row": 0, "col": 2, "value": 1 / 3**.5 },
        { "row": 7, "col": 2, "value": 1 / 3**.5 },
        { "row": 8, "col": 2, "value": 1 / 3**.5 }
    ]
    bag_of_words = { 
        "chess": 0, "abstract": 1, "board": 2, "game": 3, "playing": 4, "really": 5, "fun": 6, "king": 7, "piece": 8
    }
    query = "king chess piece"
    query_dict = { 7: "king", 0: "chess", 8: "piece" }
    query_vector = np.array([1, 0, 0, 0, 0, 0, 0, 1, 1])
    magnitudes = [(2, 1), (1, 2 / 21**.5), (0, 1 / (2 * 3**.5))]
    # tokens = [tokenize(sentence.lower()) for sentence in sentences]
    # words_dicts: list[dict[str, int]] = [
    #     { "chess": 0, "is": 0, "an": 0, "abstract": 0, "board": 0, "game": 0 },
    #     { "play": 0, "chess": 0, "is": 0, "realli": 0, "fun": 0 },
    #     { "king": 0, "is": 0, "a": 0, "chess": 0, "piec": 0 }
    # ]
    # final_words_dicts: list[dict[str, int]] = [
    #     { "chess": 0, "is": 1, "an": 2, "abstract": 3, "board": 4, "game": 5 },
    #     { "play": 0, "chess": 1, "is": 2, "realli": 3, "fun": 4 },
    #     { "king": 0, "is": 1, "a": 2, "chess": 3, "piec": 4 }
    # ]
    # frequency_vectors: list[dict[str, int]] = [
    #     { "chess": 1, "is": 1, "an": 1, "abstract": 1, "board": 1, "game": 1 },
    #     { "play": 1, "chess": 2, "is": 1, "realli": 1, "fun": 1 },
    #     { "king": 1, "is": 1, "a": 1, "chess": 1, "piec": 1 }
    # ]
    # document_frequencies: list[list[int]] = [
    #     [1, 1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1],
    #     [1, 1, 1, 1, 1]
    # ]

    def test_words_dict(self):
        res = sr.search(
            TestSearch.normalized_sparse_matrix,
            (9, 3),
            TestSearch.bag_of_words,
            TestSearch.query,
            3
        )
        print("\n\n", res, "\n")
        for i in range(len(res)):
            self.assertEqual(res[i][0], TestSearch.magnitudes[i][0])
            self.assertAlmostEqual(res[i][1], TestSearch.magnitudes[i][1])


if __name__ == "__main__":
    ut.main()