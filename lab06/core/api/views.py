from django.shortcuts import render
from django.http import HttpResponse
from copy import copy
import json
from mediawiki_dump.tokenizer import tokenize
import math
import numpy as np
from django.core.cache import cache
import db.init
import db.storage as storage
from time import time

import nltk
nltk.download('punkt')


def search(request):
    # print(np.linalg.svd(np.array([[1, 4], [0, 1], [2, 3]])))
    # storage.sparse_matrix_dims = (3, 2)
    # storage.U, storage.D, storage.V = np.linalg.svd(np.array([[1, 2], [0, 1], [2, 3]]))

    # K, m, n = db.init.K, 3, 2
    # S = np.zeros((K, n))
    # storage.S = S
    # for i in range(K):
    #     for j in range(n):
    #         S[i][j] = storage.D[i] * storage.V[i][j]

    # norms2 = np.zeros(n)
    # for i in range(K):
    #     for j in range(n):
    #         norms2[j] += S[i][j]**2
    # norms2 = np.array([n**.5 for n in norms2])

    # for i in range(K):
    #     for j in range(n):
    #         S[i][j] /= norms2[j]
    # cache.set("S", storage.S)

    # query = { 0: "chess" }

    print("Looking for most relavant documents...")
    if cache.get("sparse_matrix") is None and (db.init.K is None or db.init.K < 1 or cache.get("S") is None):
        db.init.create()

    q = np.array(tokenize(request.GET.get("q", "")))
    query = {}
    for word in q:
        if storage.bow.get(word) is not None:
            query[storage.bow.get(word)] = word
    query_norm = len(query)**.5

    k = int(request.GET.get("k", "0"))
    # print(query, k)

    #
    # Evaluate partially document frequencies (q^T U_k s_j) including query vector (cos(\phi))
    #
    if db.init.K is not None and db.init.K >= 1:
        query = np.array([1 if query.get(i) is not None else 0 for i in range(storage.sparse_matrix_dims[0])])
        v = np.zeros(db.init.K)

        start = time()

        for i in range(storage.sparse_matrix_dims[0]):
            if query[i]:
                for j in range(db.init.K):
                    v[j] += query[i] * storage.U[i][j]
        magnitudes = np.array([np.matmul(v, storage.S[:, j]) / query_norm for j in range(storage.sparse_matrix_dims[1])])
        M = np.array([(abs(magnitude), i) for i, magnitude in enumerate(magnitudes)])

        print(f"{time() - start} s")
    #
    # Evaluate document frequencies (q^T d_j) including query vector (cos(\theta))
    #
    else:
        ds = np.zeros(storage.sparse_matrix_dims[1])
        for el in storage.sparse_matrix:
            if query.get(el["row"]) is not None:
                ds[el["col"]] += el["value"]

        magnitudes = np.array([d / query_norm for d in ds])
        M = np.array([(abs(magnitude), i) for i, magnitude in enumerate(magnitudes)])

    print(np.sort(M, axis=0)[::-1][:k])

    return HttpResponse()

def count(request):
    # c = 0
    # with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/core/chesswiki.xml", "r") as file:
    #     c = WikiParser(file).count()

    return HttpResponse()