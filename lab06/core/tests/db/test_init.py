import unittest as ut
from mediawiki_dump.tokenizer import tokenize
import db.init as dbi

class TestInit(ut.TestCase):
    sentences = [
        "Chess is an abstract board game.",
        "Playing chess is really fun.",
        "King is a chess piece."
    ]
    tokens = [tokenize(sentence.lower()) for sentence in sentences]

    def test_words_dict(self):
        correct_words_dict = [
            { "chess": 0, "is": 0, "an": 0, "abstract": 0, "board": 0, "game": 0 },
            { "play": 0, "chess": 0, "is": 0, "realli": 0, "fun": 0 },
            { "king": 0, "is": 0, "a": 0, "chess": 0, "piec": 0 }
        ]

        for i, tokens in enumerate(TestInit.tokens):
            self.assertDictEqual(dbi.words_dict(tokens), correct_words_dict[i])

    def test_frequency_vector(self):
        # correct_vectors = [

        # ]
        # self.assertEqual(dbi.frequency_vector(tokens), )
        pass

    def test_sparse_matrix(self):
        pass

    def test_document_frequency(self):
        pass


if __name__ == "__main__":
    ut.main()