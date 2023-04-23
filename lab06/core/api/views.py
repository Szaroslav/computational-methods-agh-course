from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
import json
import numpy as np
import db.init
import db.storage as storage
import db.constants as constants
import api.search as sr

import nltk
nltk.download('punkt')


def search(request):
    print("Looking for most relavant documents...")
    if cache.get("sparse_matrix") is None and (db.init.K is None or db.init.K < 1 or cache.get("S") is None):
        db.init.create()

    q = request.GET.get("q", "")
    k = int(request.GET.get("k", "0"))

    M = sr.search(storage.sparse_matrix, storage.sparse_matrix_dims, storage.bow, q, k, constants.K)
    print(M)

    #
    # Return documents content
    #
    return HttpResponse(json.dumps(storage.get_contents(np.array([i for i, _ in M], dtype=np.uint16))), content_type="application/json")

def count(request):
    # c = 0
    # with open("/home/szary/Studia/4s/mownit/computation-methods-agh-course/lab06/db/core/chesswiki.xml", "r") as file:
    #     c = WikiParser(file).count()

    return HttpResponse()