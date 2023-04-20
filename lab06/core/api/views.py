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

import nltk
nltk.download('punkt')


def search(request):
    if cache.get("sparse_matrix") is None or db.init.K is not None and db.init.K >= 1 and cache.get("S") is None:
        db.init.load()

    q = np.array(tokenize(request.GET.get("q", "")))
    query = {}
    for word in q:
        if storage.bow.get(word) is not None:
            query[storage.bow.get(word)] = word
    query_norm = len(query)

    k = int(request.GET.get("k", "0"))
    # print(query, k)

    #
    # Evaluate partially document frequencies (q^T U_k s_j) including query vector (cos(\phi))
    #
    if db.init.K is not None and db.init.K >= 1:
        # ds = np.zeros(storage.sparse_matrix_dims[1])
        # for el in storage.sparse_matrix:
        #     if query.get(el["row"]) is not None:
        #         ds[el["col"]] += el["value"]
        query = np.array([query.get(i) if query.get(i) is not None else 0 for i in range(storage.sparse_matrix_dims[0])])

        magnitudes = np.array([
            np.matmul(np.matmul(query, storage.U), storage.S[:, j])[0] / query_norm for j in range(db.init.K)
        ])
        M = np.array([(abs(magnitude), i) for i, magnitude in enumerate(magnitudes)])
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

    print(np.sort(M, axis=-1)[:k])
    print(np.sort(M, axis=0)[::-1][:k])
    # print(cache.get("sparse_matrix"))

    return HttpResponse(json.dumps(query))

def count(request):
    # c = 0
    # with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/core/chesswiki.xml", "r") as file:
    #     c = WikiParser(file).count()

    return HttpResponse()