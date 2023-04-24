import numpy as np
import db.init
import db.storage as storage
from time import time
from mediawiki_dump.tokenizer import tokenize


def search(query, dims, bow, **kwargs) -> np.ndarray:
    K = kwargs.get("K")
    k = min(kwargs["k"], dims[1]) if kwargs.get("k") else 1
    q = np.array(tokenize(query))

    query = {}
    for word in q:
        if bow.get(word) is not None:
            query[bow.get(word)] = word
    query_norm = len(query)**.5

    if query_norm <= 0:
        indicies = np.arange(dims[1])
        np.random.shuffle(indicies)
        return np.array([(i, 0) for i in indicies[:k]])

    #
    # Evaluate partially document frequencies (q^T U_k s_j) including query vector (cos(\phi))
    #
    if K is not None and K >= 1:
        U, S = kwargs.get("U"), kwargs.get("S")
        query = np.array([1 if query.get(i) is not None else 0 for i in range(dims[0])])
        v = np.zeros(K)

        start = time()

        for i in range(dims[0]):
            if query[i]:
                for j in range(K):
                    v[j] += query[i] * U[i][j]
        M = np.array([abs((v @ S[:, j]) / query_norm) for j in range(dims[1])])

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
        sparse = kwargs.get("sparse")

        ds = np.zeros(dims[1])
        for el in sparse:
            if query.get(el["row"]) is not None:
                ds[el["col"]] += el["value"]

        M = np.array([abs(d / query_norm) for d in ds])

    indicies = np.argsort(M)[::-1][:k]
    return np.array([(i, M[i]) for i in indicies])
