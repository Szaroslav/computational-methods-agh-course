import unittest as ut
from mediawiki_dump.tokenizer import tokenize
import api.search as sr
import numpy as np

from scipy.sparse.linalg import svds
from scipy.sparse import csc_array


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
    query_norm2 = 3**.5
    magnitudes_sparse = [(2, 1), (1, 2 / 21**.5), (0, 1 / (2 * 3**.5))]

    #
    # Partial SVD
    #
    U = np.array([
            [-2.22044605e-16,  8.21920919e-01],
            [-5.16397779e-01,  1.40400855e-01],
            [-5.16397779e-01,  1.40400855e-01],
            [-5.16397779e-01,  1.40400855e-01],
            [ 2.58198890e-01,  2.80801709e-01],
            [ 2.58198890e-01,  2.80801709e-01],
            [ 2.58198890e-01,  2.80801709e-01],
            [ 1.28197512e-16,  1.19916646e-01],
            [ 1.28197512e-16,  1.19916646e-01]
    ])
    D = np.array([
        [1.73205081, 0],
        [0, 2.97558431]
    ])
    V = np.array([
        [-8.94427191e-01, 4.47213595e-01,  2.22044605e-16],
        [ 4.17774579e-01, 8.35549159e-01,  3.56822090e-01]
    ])
    S = D @ V
    S_norms2 = [1.9862920226405196, 2.6041167379764754, 1.0617542124654078]
    magnitudes_svd = [(2, 0.6130040795340687), (1, 0.585257761964524), (0, 0.38364941175979644)]

    #
    # Sparse matrix
    #
    def test_search_sparse(self):
        # m, n = (9, 3)
        # rows, cols, values = [], [], []
        # for el in TestSearch.sparse_matrix:
        #     rows.append(el["row"])
        #     cols.append(el["col"])
        #     values.append(el["value"])
        # sm = csc_array((values, (rows, cols)), shape=(m, n), dtype=np.float64)
        # U, D, V = svds(sm, k=2)
        # print("\n", U, D, V, "\n", sep="\n")

        res = sr.search(
            TestSearch.query,
            (9, 3),
            TestSearch.bag_of_words,
            sparse=TestSearch.normalized_sparse_matrix,
            k=3
        )
        
        for i in range(len(res)):
            self.assertEqual(res[i][0], TestSearch.magnitudes_sparse[i][0])
            self.assertAlmostEqual(res[i][1], TestSearch.magnitudes_sparse[i][1])

    #
    # Partial SVD
    #
    def test_search_svd(self):
        U, S, V = TestSearch.U, TestSearch.S, TestSearch.V
        S = np.array([[S[i][j] / TestSearch.S_norms2[j] for j in range(len(S[0]))] for i in range(len(S))])
        # q, qn = TestSearch.query_vector, TestSearch.query_norm2
        # magnitudes_svd = [(q @ U @ S[:, i]) / (qn * np.linalg.norm(S[:, i])) for i in range(len(TestSearch.V[0]))]
        # print("\n\n", magnitudes_svd, "\n")

        res = sr.search(
            TestSearch.query,
            (9, 3),
            TestSearch.bag_of_words,
            U=U,
            S=S,
            k=3,
            K=2
        )

        for i in range(len(res)):
            self.assertEqual(res[i][0], TestSearch.magnitudes_svd[i][0])
            self.assertAlmostEqual(res[i][1], TestSearch.magnitudes_svd[i][1])


if __name__ == "__main__":
    ut.main()