import numpy as np
import db.init
import db.storage as storage
from time import time
from mediawiki_dump.tokenizer import tokenize


def search(sparse, dims, bow, q, k) -> np.ndarray:
    k = min(k, dims[1])
    q = np.array(tokenize(q))
    query = {}
    for word in q:
        if bow.get(word) is not None:
            query[bow.get(word)] = word
    query_norm = len(query)**.5

    if query_norm <= 0:
        indicies = np.arange(dims[1])
        np.random.shuffle(indicies)
        return np.array([(0, i) for i in indicies[:k]])

    #
    # Evaluate partially document frequencies (q^T U_k s_j) including query vector (cos(\phi))
    #
    if db.init.K is not None and db.init.K >= 1:
        query = np.array([1 if query.get(i) is not None else 0 for i in range(dims[0])])
        v = np.zeros(db.init.K)

        start = time()

        for i in range(dims[0]):
            if query[i]:
                for j in range(db.init.K):
                    v[j] += query[i] * storage.U[i][j]
        M = np.array([abs((v @ storage.S[:, j]) / query_norm) for j in range(dims[1])])

        print(f"{time() - start} s")
    #
    # Evaluate document frequencies (q^T d_j) including query vector (cos(\theta))
    #
    else:
        # is_query_valid = False
        # for q in query:
        #     if bow.get(q) is not None:
        #         is_query_valid = True
        #         break
        # if not is_query_valid:

        ds = np.zeros(dims[1])
        for el in sparse:
            if query.get(el["row"]) is not None:
                ds[el["col"]] += el["value"]

        M = np.array([abs(d / query_norm) for d in ds])

    indicies = np.argsort(M)[::-1][:k]
    XD = np.array([(i, M[i]) for i in indicies])
    return np.array([(i, M[i]) for i in indicies])
