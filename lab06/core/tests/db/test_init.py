import unittest as ut
from mediawiki_dump.tokenizer import tokenize
import db.init as dbi
import numpy as np


class TestInit(ut.TestCase):
    sentences = [
        "Chess is an abstract board game.",
        "Playing chess is really fun. Chess.",
        "King is a chess piece."
    ]
    tokens = [tokenize(sentence.lower()) for sentence in sentences]
    words_dicts: list[dict[str, int]] = [
        { "chess": 0, "is": 0, "an": 0, "abstract": 0, "board": 0, "game": 0 },
        { "play": 0, "chess": 0, "is": 0, "realli": 0, "fun": 0 },
        { "king": 0, "is": 0, "a": 0, "chess": 0, "piec": 0 }
    ]
    final_words_dicts: list[dict[str, int]] = [
        { "chess": 0, "is": 1, "an": 2, "abstract": 3, "board": 4, "game": 5 },
        { "play": 0, "chess": 1, "is": 2, "realli": 3, "fun": 4 },
        { "king": 0, "is": 1, "a": 2, "chess": 3, "piec": 4 }
    ]
    frequency_vectors: list[dict[str, int]] = [
        { "chess": 1, "is": 1, "an": 1, "abstract": 1, "board": 1, "game": 1 },
        { "play": 1, "chess": 2, "is": 1, "realli": 1, "fun": 1 },
        { "king": 1, "is": 1, "a": 1, "chess": 1, "piec": 1 }
    ]
    document_frequencies: list[list[int]] = [
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]

    def test_words_dict(self):
        for i, tokens in enumerate(TestInit.tokens):
            self.assertDictEqual(dbi.words_dict(tokens), TestInit.words_dicts[i])

    def test_frequency_vector(self):
        for i, tokens in enumerate(TestInit.tokens):
            self.assertDictEqual(dbi.frequency_vector(tokens), TestInit.frequency_vectors[i])

    def test_sparse_matrix(self):
        correct_matrices = [
            (
                [0, 1, 2, 3, 4, 5],
                [0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1]
            ),
            (
                [0, 1, 2, 3, 4],
                [1, 1, 1, 1, 1],
                [1, 2, 1, 1, 1]
            ),
            (
                [0, 1, 2, 3, 4],
                [2, 2, 2, 2, 2],
                [1, 1, 1, 1, 1]
            )
        ]

        for i, tokens in enumerate(TestInit.tokens):
            self.assertEqual(
                dbi.sparse_matrix(TestInit.frequency_vectors[i], TestInit.final_words_dicts[i], i),
                correct_matrices[i]
            )

    def test_document_frequency(self):     
        for i, tokens in enumerate(TestInit.tokens):
            self.assertSequenceEqual(
                dbi.document_frequency(TestInit.frequency_vectors[i], TestInit.final_words_dicts[i]).tolist(),
                TestInit.document_frequencies[i]
            )

    def __flatten_tokens() -> list[str]:
        return [t for tokens in TestInit.tokens for t in tokens]


if __name__ == "__main__":
    ut.main()